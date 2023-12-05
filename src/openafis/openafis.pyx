# distutils: language = c++

from libc.stdint cimport uint8_t, uint32_t

from OpenAFIS cimport TemplateISO19794_2_2005, Fingerprint, MatchSimilarity, Param

# Create a Python class that wraps the C++ class
cdef class PyTemplateISO19794_2_2005:
    cdef TemplateISO19794_2_2005[uint32_t, Fingerprint]* c_instance

    def __cinit__(self, id: int):
        self.c_instance = new TemplateISO19794_2_2005[uint32_t, Fingerprint](id)

    def __dealloc__(self):
        del self.c_instance

    def load(self, path: str):
        return self.c_instance.load(path.encode())

    # cdef fingerprint(self):
    #     return self.c_instance.fingerprints().at(0)

cdef class PyMatchSimilarity:
    cdef MatchSimilarity* c_instance
    cdef Param param

    def __cinit__(
        self,
        MaximumLocalDistance = None,
        MaximumGlobalDistance = None,
        MinimumMinutiae = None,
        MaximumRotations = None,
        MaximumAngleDifference = None,
        MaximumDirectionDifference = None,
    ):
        self.c_instance = new MatchSimilarity()
        if MaximumLocalDistance is not None:
            self.param.MaximumLocalDistance = MaximumLocalDistance
        if MaximumGlobalDistance is not None:
            self.param.MaximumGlobalDistance = MaximumGlobalDistance
        if MinimumMinutiae is not None:
            self.param.MinimumMinutiae = MinimumMinutiae
        if MaximumRotations is not None:
            self.param.MaximumRotations = MaximumRotations
        if MaximumAngleDifference is not None:
            self.param.MaximumAngleDifference = MaximumAngleDifference
        if MaximumDirectionDifference is not None:
            self.param.MaximumDirectionDifference = MaximumDirectionDifference

    def __dealloc__(self):
        del self.c_instance

    def compute(
        self, template1: PyTemplateISO19794_2_2005, template2: PyTemplateISO19794_2_2005
    ):
        cdef uint8_t s = 0
        self.c_instance.compute(
            s,
            template1.c_instance.fingerprints().at(0),
            template2.c_instance.fingerprints().at(0),
            self.param,
        )
        return s
