# GET
https://www.oslo.kommune.no/xmlhttprequest.php?service=ren.search
&street={street}
&number={number}
&letter={letter}
&street_id={street_id}

# Types
data.result (Array)
{
  Lopenummer: string,
  Gatenavn: string,
  Gatekode: number,
  Husnummer: number,
  Bokstav: string,
  HentePunkts: {
    Id: number,
    Navn: string,
    Gatenavn: string,
    Gatekode: number,
    Husnummer: number,
    Bokstav: string,
    EurefX: number,
    EurefY: number,
    WgsX: double,
    WsgY: double,
    Tjenester: Array {
      TjenesteId: number,
      AntallBeholdere: number,
      Beholder: {
        Id: number,
        Beskrivelse: string,
        Volum: number
      },
      Fraksjon: {
        Id: number,
        Tekst: string
      },
      TommeDato: string,
      Hyppighet: {
        Faktor: number,
        Tekst: string
      },
      TommeUkedag: string
    }
  }
