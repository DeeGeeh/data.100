import pandas as pd
import json

def municipalityCodeToName(code, kunta_codes):
    # Return the name of the municipality with the given code, or None if not found
    return kunta_codes.get(str(code), None)

def toDatetime(date_str):
    if pd.isna(date_str):
        return pd.NaT
    # Jos muoto YYYY0000, korvaa 0000 -> 0101
    if isinstance(date_str, str) and len(date_str) == 8 and date_str[-4:] == "0000":
        date_str = date_str[:4] + "0101"
    # Jos muoto YYYYMMDD (esim. 19840101)
    if isinstance(date_str, str) and len(date_str) == 8 and date_str.isdigit():
        return pd.to_datetime(date_str, format="%Y%m%d", errors="coerce")
    # Jos muoto DD.MM.YYYY
    try:
        return pd.to_datetime(date_str, format="%d.%m.%Y", errors="coerce")
    except Exception:
        return pd.NaT

def fixBrandNames(df):
    print("Fixing brand names...")
    df = df.copy()
    # 1. Chrysler-erikoistapaukset kaupallinenNimi perusteella
    df.loc[df["kaupallinenNimi"].isin(["SEBRING", "CROSSFIRE"]), "merkkiSelvakielinen"] = "Chrysler"
    # 2. Daimler/XJ -> Jaguar
    mask = (df["kaupallinenNimi"] == "XJ") & (df["merkkiSelvakielinen"] == "Daimler")
    df.loc[mask, "merkkiSelvakielinen"] = "Jaguar"
    # 3. Muut korvaukset
    replacements = {
        # Audi
        "QUATTRO": "Audi", "Quattro": "Audi",
        # BMW
        "ALPINA": "BMW", "Alpina": "BMW", "BMW Alpina": "BMW", "BMW i": "BMW", "BWW": "BMW",
        # Daewoo
        "GM Daewoo": "Daewoo",
        # Ford
        "FORD-CNG-TECHNIK": "Ford", "Ford-TEC": "Ford",
        # Hyundai
        "Hundai": "Hyundai",
        # Jaguar
        "Jaguar Land Rover Limited": "Jaguar",
        # Lada
        "Lada-Vaz": "Lada", "Niva": "Lada",
        # Mercedes-Benz
        "DaimlerChrysler": "Mercedes-Benz", "Daimler": "Mercedes-Benz", "MERCEDES-AMG": "Mercedes-Benz", "Mercedes-AMG": "Mercedes-Benz", "Mercedes-Benz-CI": "Mercedes-Benz",
        # Mini
        "BMW MINI": "Mini",
        # Polestar
        "POLESTAR": "Polestar",
        # Saleen
        "SALEEN": "Saleen",
        # Skoda
        "SKD": "Skoda", "Skida": "Skoda",
        # Tesla
        "TESLA MOTORS": "Tesla", "Tesla Motors": "Tesla",
        # Think
        "THINK": "Think",
        # Toyota
        "TOYOTA": "Toyota",
        # Volkswagen
        "VOLKSWAGEN": "Volkswagen", "VW": "Volkswagen", "Volkswagen, VW": "Volkswagen"
    }
    df["merkkiSelvakielinen"] = df["merkkiSelvakielinen"].replace(replacements)
    # 4. Sallitut merkit
    allowed = [
        "Acura", "Alfa Romeo", "Aston Martin", "Audi", "BMW", "Bentley", "Buick", 
        "Cadillac", "Chevrolet", "Chrysler", "Citroen", "Cupra", "DS", "Dacia", 
        "Daewoo", "Daihatsu", "Dodge", "Ferrari", "Fiat", "Ford", "Honda", "Hyundai", 
        "Infiniti", "Jaguar", "Jeep", "Kia", "Lada", "Lamborghini", "Lancia", 
        "Land Rover", "Lexus", "Lincoln", "Lotus", "MAN", "MCC", "MG", "MINI", 
        "Maserati", "Maybach", "Mazda", "Mercedes-Benz", "Mini", "Mitsubishi", 
        "Morgan", "Nissan", "Opel", "Peugeot", "Plymouth", "Pontiac", "Porsche", 
        "Range Rover", "Renault", "Rolls-Royce", "Rover", "Saab", "Saleen", "Scion", 
        "Seat", "Skoda", "Smart", "Ssangyong", "Subaru", "Suzuki", "Tesla", "Think", 
        "Toyota", "Vauxhall", "Volkswagen", "Volvo"
    ]
    df = df[df["merkkiSelvakielinen"].isin(allowed)]
    return df

def filterRows(df, kunta_codes):
    print("Filtering rows...")
    # Filter out for rows where col ajoneuvoluokka is M1 or M1G
    df_modified = df[df["ajoneuvoluokka"].isin(["M1", "M1G"])]

    # Filter out for rows where col ajoneuvonkaytto is 1.0
    df_modified = df_modified[df_modified["ajoneuvonkaytto"] == 1.0]

    wanted_korityyppi = ["AA", "AB", "AC", "AD", "AE", "1.7"]
    df_modified = df_modified[df_modified["korityyppi"].isin(wanted_korityyppi)]

    # Filter out for rows where col kayttovaoima is na
    df_modified = df_modified[df_modified["kayttovoima"].notna()]

    # Korvaa kunta-koodit nimillä
    df_modified = df_modified.copy()
    df_modified["kunta_nimi"] = df_modified["kunta"].apply(lambda x: municipalityCodeToName(x, kunta_codes))

    # Poista rivit, joilta puuttuu kuntatieto tai joiden kunnan nimi on Tuntematon, Ulkomaat tai Pohjoismaat
    df_modified = df_modified[df_modified["kunta"].notna()]

    # Muunna päivämäärät datetimeksi ja käsittele vuosipäivät
    df_modified["kayttoonottopvm"] = df_modified["kayttoonottopvm"].apply(toDatetime)
    df_modified["ensirekisterointipvm"] = df_modified["ensirekisterointipvm"].apply(toDatetime)

    # Poista rivit, joilta puuttuu jompikumpi päivämäärä
    df_modified = df_modified[df_modified["kayttoonottopvm"].notna() & df_modified["ensirekisterointipvm"].notna()]

    # Valitse vain halutut sarakkeet, ja käytä kunta_nimi-saraketta
    wanted_cols = [
        "ensirekisterointipvm",
        "kayttoonottopvm",
        "vari",
        "omamassa",
        "ajonKokPituus",
        "ajonLeveys",
        "kayttovoima",
        "merkkiSelvakielinen",
        "mallimerkinta",
        "kaupallinenNimi",
        "kunta_nimi",
        "NEDC_Co2",
        "matkamittarilukema"
    ]
    df_modified = df_modified[wanted_cols]

    # Jos käyttövoima on 4.0 asetetaan CO2-arvoksi 0
    df_modified.loc[df_modified["kayttovoima"] == 4.0, "NEDC_Co2"] = 0

    # Jos vari on -1 aseta pd.NA
    df_modified.loc[df_modified["vari"] == -1, "vari"] = pd.NA

    df_modified = fixBrandNames(df_modified)

    return df_modified

def main():
    dtype_schema = {
        "ajoneuvoluokka": str,
        "ensirekisterointipvm": str,
        "ajoneuvoryhma": str,
        "ajoneuvonkaytto": float,
        "variantti": str,
        "versio": str,
        "kayttoonottopvm": "Int64",
        "vari": str,
        "ovienLukumaara": float,
        "korityyppi": str,
        "ohjaamotyyppi": float,
        "istumapaikkojenLkm": float,
        "omamassa": float,
        "teknSuurSallKokmassa": float,
        "tieliikSuurSallKokmassa": float,
        "ajonKokPituus": float,
        "ajonLeveys": float,
        "ajonKorkeus": float,
        "kayttovoima": str,
        "iskutilavuus": float,
        "suurinNettoteho": float,
        "sylintereidenLkm": float,
        "ahdin": str,
        "sahkohybridi": str,
        "sahkohybridinluokka": float,
        "merkkiSelvakielinen": str,
        "mallimerkinta": str,
        "vaihteisto": str,
        "vaihteidenLkm": float,
        "kaupallinenNimi": str,
        "voimanvalJaTehostamistapa": float,
        "tyyppihyvaksyntanro": str,
        "yksittaisKayttovoima": float,
        "kunta": float,
        "NEDC_Co2": float,
        "NEDC2_Co2": float,
        "WLTP_Co2": float,
        "WLTP2_Co2": float,
        "matkamittarilukema": float,
        "valmistenumero2": str,
        "jarnro": "Int64" 
    }

    df = pd.read_csv("Ajoneuvojen_avoin_data_5_27.csv", sep=";", encoding="iso8859-1", dtype=dtype_schema)
    print("Reading data...")

    with open("kuntakoodit.json", "r") as f:
        kunta_list = json.load(f)
        # Muunna listasta dict: {koodi: nimi}
        kunta_codes = {str(koodi): nimi for koodi, nimi in kunta_list}
    print("Loading kunta_codes...")

    filtered_df = filterRows(df, kunta_codes)
    filtered_df.to_csv("ajoneuvodata.csv", index=False)
    
    print("Ajoneuvodata saved to ajoneuvodata.csv")

if __name__ == "__main__":
    main()