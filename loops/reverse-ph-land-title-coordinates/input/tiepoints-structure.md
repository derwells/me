# TitlePlotterPH tiepoints.json Structure

Source: `github.com/isaacenage/TitlePlotterPH/resources/tiepoints.json`
File size: 16.6 MB (16,645,674 bytes)

## JSON Structure

Top-level: **JSON array** of objects (not nested, not keyed by province).

Each record has exactly 6 fields:

```json
{
  "Tie Point Name": "BLLM 1",
  "Description": "BLLM No. 1, Cad 614-D, Municipality of Botolan, Province of Zambales",
  "Province": "ZAMBALES",
  "Municipality": "BOTOLAN",
  "Northing": 1691760.514,
  "Easting": 394854.244
}
```

### Field Details

| Field | Type | Nulls | Notes |
|-------|------|-------|-------|
| `Tie Point Name` | string | 0 | Short identifier (e.g., "BLLM 1", "BBM 22", "AGN 131") |
| `Description` | string (1 int) | 0 | Full description with survey ref, municipality, province. 1 record has integer `10` instead of string. |
| `Province` | string | 0 | Always present, uppercase (mostly). 117 unique values. |
| `Municipality` | string/null | 2,907 nulls | null for PRS 92 control points and some older records |
| `Northing` | number (1 str) | 0 | PRS-92 / Luzon 1911 Northing in meters. 1 record has `" "` string. |
| `Easting` | number | 0 | PRS-92 / Luzon 1911 Easting in meters |

## Statistics

- **Total records: 85,303**
- **Unique provinces: 117** (includes some cities listed as provinces, e.g., MANILA, QUEZON CITY, MAKATI)
- **Unique province-municipality combos: 1,983**
- **Records with null Municipality: 2,907** (516 are PRS 92 type, 2,391 are other types)

### Coordinate Ranges (85,302 numeric records)

- **Northing**: 517,288.414 to 2,299,151.130
- **Easting**: 54,725.020 to 1,116,895.955

These are Philippine Transverse Mercator (PTM) coordinates in the PRS-92 or Luzon 1911 datum.

## Record Types by Description Pattern

| Type | Count | Description |
|------|-------|-------------|
| BBM (Bureau of Lands Boundary Monument) | 26,155 | Cadastral boundary markers |
| BLLM (Bureau of Lands Location Monument) | 19,568 | Cadastral location markers |
| PRS 92 geodetic control point | 15,609 | Modern geodetic control points |
| MBM (Municipal Boundary Monument) | 9,174 | Municipal boundary markers |
| BLBM (Barrio Location Boundary Monument) | 4,850 | Barrio-level markers |
| Monument | 1,372 | General monuments |
| Triangulation Station | 1,085 | C&GS triangulation stations |
| PBM (Provincial Boundary Monument) | 788 | Provincial boundary markers |
| Other | 6,702 | P-points, boundary descriptions, church towers, misc |

## Top Tie Point Name Prefixes

| Prefix | Count | Likely Meaning |
|--------|-------|---------------|
| BBM | 26,136 | Bureau of Lands Boundary Monument |
| BLLM | 19,611 | Bureau of Lands Location Monument |
| MBM | 9,258 | Municipal Boundary Monument |
| BLBM | 4,834 | Barrio Location Boundary Monument |
| MON | 1,258 | Monument |
| TS | 928 | Triangulation Station |
| QZN | 846 | Quezon province code |
| PBM | 791 | Provincial Boundary Monument |
| PNG | 727 | Pangasinan province code |
| CGY | 661 | Cagayan province code |

Province-coded prefixes (PRS 92 control points): ISB, DVS, SRN, ZBS, PMG, BLN, NEJ, BKN, CBU, TRC, CVT, LYT, BHL, etc.

## Records Per Province (Top 30)

| Province | Records |
|----------|---------|
| ILOILO | 4,618 |
| PANGASINAN | 4,363 |
| QUEZON | 4,288 |
| BOHOL | 3,265 |
| BATANGAS | 2,841 |
| CAMARINES SUR | 2,702 |
| BULACAN | 2,642 |
| NEGROS OCCIDENTAL | 2,443 |
| PAMPANGA | 2,399 |
| LEYTE | 2,273 |
| LAGUNA | 2,098 |
| NUEVA ECIJA | 2,052 |
| ILOCOS NORTE | 1,845 |
| CAVITE | 1,813 |
| LA UNION | 1,717 |
| PALAWAN | 1,686 |
| TARLAC | 1,611 |
| CAGAYAN | 1,604 |
| CEBU | 1,562 |
| ISABELA | 1,560 |
| ILOCOS SUR | 1,495 |
| ALBAY | 1,483 |
| BUKIDNON | 1,450 |
| ORIENTAL MINDORO | 1,443 |
| ZAMBALES | 1,385 |
| DAVAO DEL SUR | 1,255 |
| DAVAO DEL NORTE | 1,159 |
| SURIGAO DEL SUR | 1,093 |
| AKLAN | 1,084 |
| CAMARINES NORTE | 1,081 |

## Datum Considerations

The coordinates are a **mix of Luzon 1911 and PRS-92 datums**:
- Records with PRS 92 in Description are explicitly in PRS-92 datum
- Older records (BBM, BLLM, MBM, etc. with Cad/Pls references) are likely in Luzon 1911 datum
- The file does NOT have a datum indicator field per record
- This is critical: coordinates from the two datums differ by ~100-300 meters

## Sample Records (35 records from diverse provinces)

```json
[
  {"Tie Point Name":"BLBM 1","Description":"BLBM No. 1, Bo. of Sta. Ines, Municipality of Sta. Ignacia, Province of Tarlac","Province":"TARLAC","Municipality":"STA. IGNACIA","Northing":1720551.189,"Easting":443738.651},
  {"Tie Point Name":"BLLM 1","Description":"BLLM No. 1, Mcadm 590-D, Municipality of Taguig, Province of Rizal","Province":"RIZAL","Municipality":"TAGUIG","Northing":1606647.046,"Easting":507862.897},
  {"Tie Point Name":"BLLM 1","Description":"BLLM No. 1, Municipality of Makati","Province":"MAKATI","Municipality":null,"Northing":1611131,"Easting":503381.8125},
  {"Tie Point Name":"AGDII","Description":"AGD II, PRS 92","Province":"ABRA","Municipality":null,"Northing":1944859.304,"Easting":461958.705},
  {"Tie Point Name":"AGN 131","Description":"AGN 131, PRS 92","Province":"AGUSAN DEL NORTE","Municipality":null,"Northing":999634.134,"Easting":1012435.334},
  {"Tie Point Name":"AKN 36","Description":"AKN 36, PRS 92","Province":"AKLAN","Municipality":null,"Northing":1323700.659,"Easting":600076.885},
  {"Tie Point Name":"ABY 3170","Description":"ABY 3170, PRS 92","Province":"ALBAY","Municipality":null,"Northing":1465055.88,"Easting":811968.03},
  {"Tie Point Name":"BTS 3","Description":"BTS 3, PRS 92","Province":"BATANES","Municipality":"BASCO","Northing":2261131.62,"Easting":600340.5},
  {"Tie Point Name":"BBM 1","Description":"BBM No. 1, Cad 857-D, Municipality of  Agoncillo, Province of Batangas","Province":"BATANGAS","Municipality":"AGONCILLO","Northing":1540788.217,"Easting":491922.503},
  {"Tie Point Name":"BGT 152","Description":"BGT 152, PRS 92","Province":"BENGUET","Municipality":null,"Northing":1853733.247,"Easting":483881.308},
  {"Tie Point Name":"BHL 3032","Description":"BHL 3032, PRS 92","Province":"BOHOL","Municipality":null,"Northing":1077013.124,"Easting":877598.576},
  {"Tie Point Name":"BKN 3400","Description":"BKN 3400, PRS 92","Province":"BUKIDNON","Municipality":null,"Northing":861656.08,"Easting":939720.863},
  {"Tie Point Name":"BLN 21","Description":"BLN 21, PRS 92","Province":"BULACAN","Municipality":null,"Northing":1684292.9,"Easting":509621.261},
  {"Tie Point Name":"CGY 3851","Description":"CGY 3851, PRS 92","Province":"CAGAYAN","Municipality":null,"Northing":1978310.392,"Easting":595845.297},
  {"Tie Point Name":"BBM 1","Description":"BBM No. 1, Pls 812-D, Municipality of Baao, Province of Camarines Sur","Province":"CAMARINES SUR","Municipality":"BAAO","Northing":1494466.742,"Easting":756431.862},
  {"Tie Point Name":"CVT 22","Description":"CVT 22, PRS 92","Province":"CAVITE","Municipality":null,"Northing":1601569.36,"Easting":489698.235},
  {"Tie Point Name":"BLLM 2","Description":"BLLM No. 2, Cad 12, Cebu Cadastre","Province":"CEBU","Municipality":null,"Northing":1139879,"Easting":818241.8125},
  {"Tie Point Name":"DVS 102","Description":"DVS 102, PRS 92","Province":"DAVAO DEL SUR","Municipality":null,"Northing":600516.568,"Easting":994994.522},
  {"Tie Point Name":"BLLM 1","Description":"BLLM No. 1, Cad 794-D, Municipality of Adams, Province of Ilocos Norte","Province":"ILOCOS NORTE","Municipality":"ADAMS","Northing":2042054.36,"Easting":489448.785},
  {"Tie Point Name":"ILO 3069","Description":"ILO 3069, PRS 92","Province":"ILOILO","Municipality":null,"Northing":1223970.211,"Easting":692923.874},
  {"Tie Point Name":"LAG 3083","Description":"LAG 3083, PRS 92","Province":"LAGUNA","Municipality":null,"Northing":1577750.1,"Easting":547208.906},
  {"Tie Point Name":"LYT 105","Description":"LYT 105, PRS 92","Province":"LEYTE","Municipality":null,"Northing":1236686.878,"Easting":931615.955},
  {"Tie Point Name":"? BLK 2253","Description":"19-Block No. 2253-I-J-9","Province":"MANILA","Municipality":null,"Northing":1616504.889,"Easting":497706.197},
  {"Tie Point Name":"BBM 22","Description":"BBM No. 22, Cad 39, Municipality of Bacolod, Province of Negros Occidental","Province":"NEGROS OCCIDENTAL","Municipality":"BACOLOD","Northing":1175003.322,"Easting":710425.382},
  {"Tie Point Name":"NEJ 3030","Description":"NEJ 3030, PRS 92","Province":"NUEVA ECIJA","Municipality":null,"Northing":1703525.97,"Easting":482573.038},
  {"Tie Point Name":"BBM 1","Description":"BBM No. 1, Cad 644-D, Municipality of Baco, Province of Oriental Mindoro","Province":"ORIENTAL MINDORO","Municipality":"BACO","Northing":1477165.92,"Easting":510158.84},
  {"Tie Point Name":"PLW 106","Description":"PLW 106, PRS 92","Province":"PALAWAN","Municipality":null,"Northing":1023039.156,"Easting":169394.805},
  {"Tie Point Name":"? INT","Description":"Intersection of Road to Porac","Province":"PAMPANGA","Municipality":null,"Northing":1662767.423,"Easting":447628.998},
  {"Tie Point Name":"PNG 4000","Description":"PNG 4000, PRS 92","Province":"PANGASINAN","Municipality":null,"Northing":1758802.514,"Easting":467768.493},
  {"Tie Point Name":"QZN 3407","Description":"QZN 3407, PRS 92","Province":"QUEZON","Municipality":null,"Northing":1631539.168,"Easting":605426.318},
  {"Tie Point Name":"? COR","Description":"NE Corner of Sen. M. Cuenco St. and Halcon St., Quezon City","Province":"QUEZON CITY","Municipality":null,"Northing":1616816.768,"Easting":499695.562},
  {"Tie Point Name":"CTS 3","Description":"CTS 3, PRS 92","Province":"SOUTH COTABATO","Municipality":null,"Northing":689991.609,"Easting":910937.062},
  {"Tie Point Name":"BLLM 1","Description":"BLLM No. 1, Cad 99, Municipality of Jolo, Province of Sulu","Province":"SULU","Municipality":"JOLO","Northing":669213.0043,"Easting":499797.0522},
  {"Tie Point Name":"SRN 3179","Description":"SRN 3179, PRS 92","Province":"SURIGAO DEL NORTE","Municipality":null,"Northing":1085968.766,"Easting":989572.825},
  {"Tie Point Name":"ZGS 91","Description":"ZGS 91, PRS 92","Province":"ZAMBOANGA DEL SUR","Municipality":null,"Northing":818899.507,"Easting":646226.476}
]
```
