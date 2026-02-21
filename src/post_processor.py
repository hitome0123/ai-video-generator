"""
后处理模块
功能：
1. 字幕合成 - 从 script.json 读取文案，用 FFmpeg 烧录到视频
2. BGM 混音  - 从 static/bgm/ 目录读取音频文件，FFmpeg 混音
"""
import subprocess
import shutil
import platform
from pathlib import Path
from typing import Optional, Dict, List


# BGM 文件目录
BGM_DIR = Path(__file__).parent.parent / "static" / "bgm"


def _find_chinese_font() -> str:
    """查找支持中文的系统字体路径"""
    system = platform.system()

    candidates = []
    if system == "Darwin":  # macOS
        candidates = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/Library/Fonts/Arial Unicode MS.ttf",
        ]
    elif system == "Linux":
        candidates = [
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    else:  # Windows
        candidates = [
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simsun.ttc",
        ]

    for path in candidates:
        if Path(path).exists():
            return path

    # 找不到中文字体，返回空字符串（drawtext 将使用默认字体，可能不支持中文）
    return ""


class PostProcessor:
    """视频后处理器"""

    def __init__(self):
        self.ffmpeg_available = shutil.which("ffmpeg") is not None
        self.font_path = _find_chinese_font()
        BGM_DIR.mkdir(parents=True, exist_ok=True)

    def add_subtitles(
        self,
        video_path: str,
        script: dict,
        output_path: str,
    ) -> Dict:
        """
        将脚本文案烧录为字幕

        从 script.json 的 scenes[].text 字段读取文案，
        按每个场景的 duration 计算时间轴，用 FFmpeg drawtext 叠加。

        Args:
            video_path: 输入视频路径
            script: 视频脚本字典（含 hook / scenes / cta）
            output_path: 输出视频路径
        """
        if not self.ffmpeg_available:
            shutil.copy2(video_path, output_path)
            return {"status": "skipped", "reason": "FFmpeg 未安装，跳过字幕"}

        scenes: List[dict] = script.get("scenes", [])
        filters: List[str] = []
        current_time = 0.0

        # Hook 字幕（开头 3 秒）
        hook = script.get("hook", "").strip()
        if hook:
            safe = _escape_drawtext(hook)
            font_opt = f":fontfile='{self.font_path}'" if self.font_path else ""
            filters.append(
                f"drawtext=text='{safe}'"
                f":fontsize=38:fontcolor=white"
                f":bordercolor=black:borderw=2"
                f":x=(w-text_w)/2:y=60"
                f"{font_opt}"
                f":enable='between(t,0,3)'"
            )
            current_time = 3.0

        # 每个场景字幕
        for scene in scenes:
            text = scene.get("text", "").strip()
            duration = float(scene.get("duration", 3))
            if text:
                safe = _escape_drawtext(text)
                font_opt = f":fontfile='{self.font_path}'" if self.font_path else ""
                start = current_time
                end = current_time + duration
                filters.append(
                    f"drawtext=text='{safe}'"
                    f":fontsize=42:fontcolor=white"
                    f":bordercolor=black:borderw=2"
                    f":x=(w-text_w)/2:y=h-90"
                    f"{font_opt}"
                    f":enable='between(t,{start:.1f},{end:.1f})'"
                )
            current_time += duration

        # CTA 字幕（最后 2 秒）
        cta = script.get("cta", "").strip()
        if cta:
            safe = _escape_drawtext(cta)
            font_opt = f":fontfile='{self.font_path}'" if self.font_path else ""
            filters.append(
                f"drawtext=text='{safe}'"
                f":fontsize=38:fontcolor=yellow"
                f":bordercolor=black:borderw=2"
                f":x=(w-text_w)/2:y=h-90"
                f"{font_opt}"
                f":enable='gte(t,{current_time:.1f})'"
            )

        if not filters:
            shutil.copy2(video_path, output_path)
            return {"status": "success", "note": "无字幕文案，跳过字幕处理"}

        vf = ",".join(filters)
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", vf,
            "-c:a", "copy",
            output_path,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ 字幕合成完成: {output_path}")
            return {"status": "success", "output": output_path}
        else:
            print(f"⚠️ 字幕合成失败，使用原视频: {result.stderr[-300:]}")
            shutil.copy2(video_path, output_path)
            return {"status": "skipped", "reason": "FFmpeg 字幕合成失败，使用原视频"}

    def add_bgm(
        self,
        video_path: str,
        output_path: str,
        volume: float = 0.25,
    ) -> Dict:
        """
        混入背景音乐

        从 static/bgm/ 目录查找第一个音频文件（mp3/wav/m4a），
        使用 FFmpeg 混音，BGM 音量为 25%。

        Args:
            video_path: 输入视频路径
            output_path: 输出视频路径
            volume: BGM 相对音量（0.0-1.0）
        """
        if not self.ffmpeg_available:
            shutil.copy2(video_path, output_path)
            return {"status": "skipped", "reason": "FFmpeg 未安装，跳过 BGM"}

        bgm_file = self._find_bgm()
        if not bgm_file:
            shutil.copy2(video_path, output_path)
            return {
                "status": "skipped",
                "reason": f"未找到 BGM 文件，请在 static/bgm/ 目录放置 mp3/wav 文件",
            }

        print(f"🎵 混入 BGM: {bgm_file.name}")

        # 尝试方式一：视频有音轨，amix 混音
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", str(bgm_file),
            "-filter_complex",
            f"[1:a]volume={volume},aloop=loop=-1:size=2e+09[bgm];"
            f"[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            output_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✅ BGM 混音完成: {output_path}")
            return {"status": "success", "output": output_path, "bgm": bgm_file.name}

        # 方式二：视频无音轨，直接添加 BGM
        cmd2 = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", str(bgm_file),
            "-map", "0:v",
            "-map", "1:a",
            "-c:v", "copy",
            "-af", f"volume={volume}",
            "-shortest",
            output_path,
        ]
        result2 = subprocess.run(cmd2, capture_output=True, text=True)

        if result2.returncode == 0:
            print(f"✅ BGM 添加完成: {output_path}")
            return {"status": "success", "output": output_path, "bgm": bgm_file.name}

        print(f"⚠️ BGM 混音失败，使用原视频")
        shutil.copy2(video_path, output_path)
        return {"status": "skipped", "reason": "BGM 混音失败，使用原视频"}

    def process(
        self,
        video_path: str,
        output_path: str,
        script: Optional[dict] = None,
        add_subtitle: bool = False,
        add_bgm: bool = False,
    ) -> Dict:
        """
        后处理主入口，按顺序执行字幕 → BGM

        Args:
            video_path: 原始视频路径
            output_path: 最终输出路径
            script: 视频脚本（字幕来源）
            add_subtitle: 是否添加字幕
            add_bgm: 是否添加 BGM
        """
        if not add_subtitle and not add_bgm:
            shutil.copy2(video_path, output_path)
            return {"status": "success", "output": output_path, "steps": []}

        tmp_dir = Path(output_path).parent
        tmp_sub = str(tmp_dir / "_tmp_subtitle.mp4")
        tmp_bgm = str(tmp_dir / "_tmp_bgm.mp4")
        steps = []
        current = video_path

        try:
            if add_subtitle and script:
                res = self.add_subtitles(current, script, tmp_sub)
                steps.append({"step": "字幕", **res})
                if res["status"] == "success":
                    current = tmp_sub

            if add_bgm:
                res = self.add_bgm(current, tmp_bgm)
                steps.append({"step": "BGM", **res})
                if res["status"] == "success":
                    current = tmp_bgm

            shutil.copy2(current, output_path)

        finally:
            for tmp in (tmp_sub, tmp_bgm):
                try:
                    Path(tmp).unlink(missing_ok=True)
                except Exception:
                    pass

        return {"status": "success", "output": output_path, "steps": steps}

    def _find_bgm(self) -> Optional[Path]:
        """从 static/bgm/ 目录查找第一个音频文件"""
        for ext in ("*.mp3", "*.wav", "*.m4a", "*.aac"):
            files = list(BGM_DIR.glob(ext))
            if files:
                return files[0]
        return None


def _escape_drawtext(text: str) -> str:
    """转义 FFmpeg drawtext 特殊字符"""
    return (
        text
        .replace("\\", "\\\\")
        .replace("'", "\u2019")   # 单引号替换为弯引号
        .replace(":", "\\:")
        .replace("[", "\\[")
        .replace("]", "\\]")
    )
