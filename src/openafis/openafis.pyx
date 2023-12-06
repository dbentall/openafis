# distutils: language = c++

from libc.stdint cimport uint8_t, uint32_t

from OpenAFIS cimport TemplateISO19794_2_2005, Fingerprint, MatchSimilarity, Param


cdef class PyTemplateISO19794_2_2005:
    """Python wrapper for OpenAFIS TemplateISO19794_2_2005 class. This represents one 
    fingerprint template. It can be loaded from an ISO19794_2_2005-compliant file or
    from a byte array.
    """
    cdef TemplateISO19794_2_2005[uint32_t, Fingerprint]* c_instance

    def __cinit__(self, id: int):
        self.c_instance = new TemplateISO19794_2_2005[uint32_t, Fingerprint](id)

    def __dealloc__(self):
        del self.c_instance

    @staticmethod
    def from_file(path: str, id: int = 0):
        py_template = PyTemplateISO19794_2_2005(id)
        py_template.c_instance.load(path.encode())
        return py_template

    @staticmethod
    def from_bytes(data: bytes, id: int = 0):
        py_template = PyTemplateISO19794_2_2005(id)
        py_template.c_instance.load(data, len(data))
        return py_template


cdef class PyMatchSimilarity:
    """Python wrapper for OpenAFIS MatchSimilarity class. This class is used to compute
    the similarity between two fingerprint templates.
    """
    cdef MatchSimilarity* c_instance
    cdef Param param

    def __cinit__(
        self,
        max_local_dist = None,
        max_global_dist = None,
        min_minutiae = None,
        max_rotations = None,
        max_angle_diff = None,
        max_direction_diff = None,
    ):
        self.c_instance = new MatchSimilarity()
        if max_local_dist is not None:
            self.param.MaximumLocalDistance = max_local_dist
        if max_global_dist is not None:
            self.param.MaximumGlobalDistance = max_global_dist
        if min_minutiae is not None:
            self.param.MinimumMinutiae = min_minutiae
        if max_rotations is not None:
            self.param.MaximumRotations = max_rotations
        if max_angle_diff is not None:
            self.param.MaximumAngleDifference = max_angle_diff
        if max_direction_diff is not None:
            self.param.MaximumDirectionDifference = max_direction_diff

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
