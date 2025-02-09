from .state import State, states


# class Value(dict):

#     def __init__(self, *args, k=8, **kwargs):
#         self.k = k
#         self.loc = threading.Lock()
#         self.sem = threading.Semaphore(k)
#         super().__init__(*args, **kwargs)

#     def __getitem__(self, key):
#         with self.loc:
#             pass
#         self.sem.acquire()
#         try:
#             return super().__getitem__(key)
#         finally:
#             self.sem.release()

#     def __setitem__(self, key, value):
#         with self.loc:
#             for _ in range(self.k):
#                 self.sem.acquire()
#         try:
#             super().__setitem__(key, value)
#         finally:
#             for _ in range(self.k):
#                 self.sem.release()

#     def items(self):
#         with self.loc:
#             return super().items()


class Value(dict[State, float]):

    def __init__(self, data=None):
        super().__init__(data if data else {state: 0. for state in states})
