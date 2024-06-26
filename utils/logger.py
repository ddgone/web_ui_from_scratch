import time
import inspect
from loguru import logger
from pathlib import Path

from config.pathconf import BASE_DIR


class Logger:
    _instance = None
    _logger_initialized = False

    # 类属性，保存配置好的logger实例
    instance = logger

    if not _logger_initialized:
        logger_path = Path(BASE_DIR, "output/logs")
        if not logger_path.exists():
            logger_path.mkdir(parents=True)
        instance.add(
            f"{logger_path}/auto_log_{time.strftime('%Y-%m-%d')}.log",
            rotation="00:00",
            encoding="utf-8",
            enqueue=True,
            retention="30 days",
            level="DEBUG",
        )
        _logger_initialized = True

    @staticmethod
    def _get_caller_depth():
        # 获取当前的堆栈
        stack = inspect.stack()
        # 检查堆栈帧以找到第一个调用点
        # 这不是 Logger 类的一部分
        for depth, frame_info in enumerate(stack):
            if frame_info.frame.f_globals.get('__name__') != __name__:
                return depth - 1
        return 0

    @staticmethod
    def trace(*args, **kwargs):
        depth = Logger._get_caller_depth()
        Logger.instance.opt(depth=depth).trace(*args, **kwargs)

    @staticmethod
    def debug(*args, **kwargs):
        depth = Logger._get_caller_depth()
        Logger.instance.opt(depth=depth).debug(*args, **kwargs)

    @staticmethod
    def info(*args, **kwargs):
        depth = Logger._get_caller_depth()
        Logger.instance.opt(depth=depth).info(*args, **kwargs)

    @staticmethod
    def warning(*args, **kwargs):
        depth = Logger._get_caller_depth()
        Logger.instance.opt(depth=depth).warning(*args, **kwargs)

    @staticmethod
    def error(*args, **kwargs):
        depth = Logger._get_caller_depth()
        Logger.instance.opt(depth=depth).error(*args, **kwargs)

    @staticmethod
    def critical(*args, **kwargs):
        depth = Logger._get_caller_depth()
        Logger.instance.opt(depth=depth).critical(*args, **kwargs)

    @staticmethod
    def exception(*args, **kwargs):
        depth = Logger._get_caller_depth()
        Logger.instance.opt(depth=depth).exception(*args, **kwargs)


# 使用示例
if __name__ == '__main__':
    Logger.debug("记录一些调试信息")
    Logger.info("记录一些一般信息")
    Logger.warning("记录一些警告信息")
    Logger.error("记录一些错误信息")
    Logger.critical("记录一些关键错误信息")
    Logger.exception("自动记录异常信息")
