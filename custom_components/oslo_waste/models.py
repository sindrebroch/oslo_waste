from enum import Enum, IntEnum
from typing import Any, Dict, List

import attr

from .const import LOGGER


@attr.s(auto_attribs=True)
class Beholder:
    """Class representing Beholder."""

    Id: int
    Beskrivelse: str
    Volum: int

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Beholder":
        """Transform data to dict."""

        LOGGER.debug("Beholder=%s", data)

        return Beholder(
            Id=int(data["Id"]),
            Beskrivelse=data["Beskrivelse"],
            Volum=int(data["Volum"]),
        )


@attr.s(auto_attribs=True)
class Fraksjon:
    """Class representing Fraksjon."""

    Id: int
    Tekst: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Fraksjon":
        """Transform data to dict."""

        LOGGER.debug("Fraksjon=%s", data)

        return Fraksjon(
            Id=int(data["Id"]),
            Tekst=data["Tekst"],
        )


@attr.s(auto_attribs=True)
class Hyppighet:
    """Class representing Hyppighet."""

    Faktor: int
    Tekst: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Hyppighet":
        """Transform data to dict."""

        LOGGER.debug("Hyppighet=%s", data)

        return Hyppighet(
            Faktor=int(data["Faktor"]),
            Tekst=data["Tekst"],
        )


@attr.s(auto_attribs=True)
class Tjeneste:
    """Class representing Tjeneste."""

    TjenesteId: int
    AntallBeholdere: int
    Beholder: Beholder
    Fraksjon: Fraksjon
    TommeDato: str
    Hyppighet: Hyppighet
    TommeUkedag: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Tjeneste":
        """Transform data to dict."""

        LOGGER.debug("Tjeneste=%s", data)

        return Tjeneste(
            TjenesteId=int(data["TjenesteId"]),
            AntallBeholdere=int(data["AntallBeholdere"]),
            Beholder=Beholder.from_dict(data["Beholder"]),
            Fraksjon=Fraksjon.from_dict(data["Fraksjon"]),
            TommeDato=data["TommeDato"],
            Hyppighet=Hyppighet.from_dict(data["Hyppighet"]),
            TommeUkedag=data["TommeUkedag"],
        )


@attr.s(auto_attribs=True)
class HentePunkt:
    """Class representing HentePunkt."""

    Id: int
    Navn: str
    Gatenavn: str
    Gatekode: int
    Husnummer: int
    Bokstav: str
    EurefX: int
    EurefY: int
    WgsX: float
    WgsY: float
    Tjenester: List[Tjeneste]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "HentePunkt":
        """Transform data to dict."""

        LOGGER.debug("HentePunkt=%s", data)

        return HentePunkt(
            Id=int(data["Id"]),
            Navn=data["Navn"],
            Gatenavn=data["Gatenavn"],
            Gatekode=int(data["Gatekode"]),
            Husnummer=int(data["Husnummer"]),
            Bokstav=data["Bokstav"],
            EurefX=int(data["EurefX"]),
            EurefY=int(data["EurefY"]),
            WgsX=float(data["WgsX"]),
            WgsY=float(data["WgsY"]),
            Tjenester=(Tjeneste.from_dict(t) for t in data["Tjenester"]),
        )


@attr.s(auto_attribs=True)
class ResponseResult:
    """Class representing Response."""

    Lopenummer: str
    Gatenavn: str
    Gatekode: int
    Husnummer: int
    Bokstav: str
    HentePunkts: List[HentePunkt]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ResponseResult":
        """Transform data to dict."""

        LOGGER.debug("ResponseResult=%s", data)

        return ResponseResult(
            Lopenummer=data["Lopenummer"],
            Gatenavn=data["Gatenavn"],
            Gatekode=int(data["Gatekode"]),
            Husnummer=int(data["Husnummer"]),
            Bokstav=data["Bokstav"],
            HentePunkts=(HentePunkt.from_dict(t) for t in data["HentePunkts"]),
        )


@attr.s(auto_attribs=True)
class ResponseData:
    """Class representing ResponseData."""

    results: List[ResponseResult]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ResponseData":
        """Transform data to dict."""

        # LOGGER.debug("ResponseData=%s", data)

        return ResponseData(
            results=(ResponseResult.from_dict(t) for t in data["data"]["result"])
        )
