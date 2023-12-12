import struct

from pydantic import BaseModel


class Minutia(BaseModel):
    """Pydantic model for a minutia in ISO 19794-2:2005.

    Type and angle are optional. Quality is not used in the current implementation.
    """
    type: int = 1
    x: int
    y: int
    angle: int = 0
    quality: int = 0


class Fingerprint(BaseModel):
    """Pydantic model for a fingerprint in ISO 19794-2:2005.

    A list of minutiae. Position and quality are not used in the current implementation.
    """
    position: int = 0
    quality: int = 0
    minutiae: list[Minutia]


class ISOFormat(BaseModel):
    """Pydantic model for ISO 19794-2:2005.

    Typically a list with a single fingerprint. Width, height, resolution_x and
    resolution_y are not used in the current implementation.
    """
    width: int = 0
    height: int = 0
    resolution_x: int = 0
    resolution_y: int = 0
    fingerprints: list[Fingerprint]

    @classmethod
    def from_iso_file(cls, path):
        fingerprints = []

        with open(path, "rb") as f:
            header = f.read(8)
            if header != b"FMR\x00 20\x00":
                raise ValueError("Invalid ISO 19794-2 file")

            # Read the header
            (
                _,
                _,
                width,
                height,
                resolution_x,
                resolution_y,
                fingerprint_count,
                _,
            ) = struct.unpack(">IHHHHHBB", f.read(16))

            # Read the fingerprints
            for _ in range(fingerprint_count):
                position, _, quality, minutiae_count = struct.unpack(">BBBB", f.read(4))
                minutiae = []
                for _ in range(minutiae_count):
                    type_x, rfu_y, angle, quality = struct.unpack(">HHBB", f.read(6))
                    x = type_x & 0x3FFF  # Lower 14 bits
                    # Extract type
                    type_ = type_x >> 14  # Upper 2 bits
                    y = rfu_y & 0x3FFF  # Lower 14 bits
                    minutiae.append(
                        Minutia(type=type_, x=x, y=y, angle=angle, quality=quality)
                    )
                fingerprints.append(
                    Fingerprint(
                        position=position,
                        quality=quality,
                        minutiae=minutiae,
                    )
                )

        return cls(
            width=width,
            height=height,
            resolution_x=resolution_x,
            resolution_y=resolution_y,
            fingerprints=fingerprints,
        )

    def to_iso_file(self, path):
        with open(path, "wb") as f:
            f.write(self.to_iso_bytes())

    def to_iso_bytes(self) -> bytes:
        # n_fingerprints * (fingerprint_header + n_minutiae * minutiae)
        fingerprint_lengths = [
            4 + len(fingerprint.minutiae) * 6 for fingerprint in self.fingerprints
        ]
        # pre-header + header + sum(fingerprint_lengths) + footer
        total_length = 8 + 16 + sum(fingerprint_lengths) + 2

        # Pre-header
        out = b"FMR\x00 20\x00"
        out += struct.pack(
            ">IHHHHHBB",
            total_length,
            0,
            self.width,
            self.height,
            self.resolution_x,
            self.resolution_y,
            len(self.fingerprints),
            0,
        )
        for fingerprint in self.fingerprints:
            out += struct.pack(
                ">BBBB",
                fingerprint.position,
                0,
                fingerprint.quality,
                len(fingerprint.minutiae),
            )
            for minutia in fingerprint.minutiae:
                type_x = (minutia.type << 14) | minutia.x
                rfu_y = minutia.y
                out += struct.pack(
                    ">HHBB",
                    type_x,
                    rfu_y,
                    minutia.angle,
                    minutia.quality,
                )
        # Footer
        out += b"\x00\x00"
        return out
