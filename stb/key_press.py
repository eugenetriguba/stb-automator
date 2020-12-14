
class KeyPress:
    def __init__(self, key: str, start_time: float, end_time: float):
        self.__key = key
        self.__start_time = start_time
        self.__end_time = end_time

    @property
    def key(self):
        return self.__key
    
    @property
    def start_time(self):
        return self.__start_time
    
    @property
    def end_time(self):
        return self.__end_time

    def __repr__(self):
        return (
            f"KeyPress(key={self.__key}, "
            f"start_time={self.__start_time}, "
            f"end_time={self.__end_time})"
        )
