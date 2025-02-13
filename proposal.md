# DATA 551: Dataviz II - Project - Proposal

**Name**: Amali Jayatileke, Kiran John, Kelsey Strachan, Jason Suwito

**Published**: February 14, 2025

## Section 1. Motivation and purpose

> **Our role**: Parks Canada Wildfire Analysts

> **Target audience**: Government of British Columbia

Wildfires are a prevalent natural phenomenon that have caused significant damage to Canadian forests and communities. By using data from the past decade, we hope to provide insights on the causes, locations, and severity of these fires. With a comprehensive dashboard, we will visualize these various facets to allow government officials to understand the wildfire landscape and identify areas to improve resource allocation. The app we create will allow users to filter on specific times, view key statistics, and change according to specific selections.

## Section 2. Description of data

We are going to use the National Fire Database fire point data (NFDFPT) to produce the thematic dashboard. The NFDFPT is a collection of forest fire locations as provided by Canadian fire management agencies including provinces, territories, and Parks Canada. The data was obtained through the Canadian Wildland Fire Information System under the Natural Resources Canada website. The data was collected across all 10 provinces and 3 territories of Canada from ​​1930 to 2023. There are 436,564 fires recorded in this dataset with 25 associated features that identifies the fire (`FID`, `NFDBFIREID`, `FIRE_ID`, `FIRENAME`), the location of the fire (`LATITUDE`, `LONGITUDE`, `NAT_PARK`, `SRC_AGENCY`, `PROTZONE`), the time of the fire (`YEAR`, `MONTH`, `DATE`, `REP_DATE`, `ATTK_DATE`, `OUT_DATE`), the characteristics of the fire (`SIZE_HA`, `CAUSE`, `CAUSE2`, `FIRE_TYPE`, `PRESCRIBED`), the measures taken to handle the fire (`RESPONSE`), and additional notes from the data collectors (`MORE_INFO`, `CFS_NOTE1`, `CFS_NOTE2`, `ACQ_DATE`). For a complete list and description of the features, refer to Appendix X. 

While the dataset is very comprehensive, most columns will not be used as part of our analysis due to their irrelevance. Additionally, we will also focus our analysis on fires that happen in the past decade (10 years) from 2013 to 2023. The reduced dataset eventually only contains 57,355 fires that happened across Canada. Furthermore, we will focus on one province, British Columbia, limiting the dataset to 15,052 fires.


## Section 3. Research questions and usage scenarios

> **Research Question 1**: What is the relationship between fire location, formal cause, and size?

> **Research Question 2**: Which regions are most impacted by wildfires within British Columbia?

The recipient is a policy maker with the Government of Canada who wants to evaluate wildfire trend data from the past 10 years. The goal is to explore the data set to assess which provinces have been most impacted by wildfires and their subsequent provincial responses. An important element in the dashboard is the fire location and formal cause, as this information may be utilized by the Government to allocate funding for provincial fire prevention. When the policy maker accesses the dashboard, they will view an overview map of Canada that will include national parks, as they hope to gather statistics on the fraction of wildfires that have impacted national parks. There will be the option to filter on a BC-specific visualization for closer inspection. The policy maker also aims for the dashboard to show overall summary statistics and to illustrate if previous wildfire mitigation strategies within British Columbia (BC) were deemed successful. The dashboard will contain features to show time trends via line charts, fire sizes, fire causes in pie chart format, and fire types per province. The policy maker aims to show that BC should receive a significant portion of the federal funding due to climate change effects even though this province does not contain national parks.

## Appendix

The following table describes the features in the dataset derived from [CWFIS Datamart](https://cwfis.cfs.nrcan.gc.ca/datamart)

| Feature      | Datatype | Description |
|-------------|---------|-------------|
| FID         | Integer | Internal feature number |
| NFDBFIREID  | String  | NRCan constructed ID by combining the following fields: SRC_AGENCY - YEAR - FIRE_ID |
| SRC_AGENCY  | String  | Agency (province, territory, parks) from which the fire data has been obtained. BC - British Columbia, AB - Alberta, SK - Saskatchewan, MB - Manitoba, ON - Ontario, QC - Quebec, NS - Nova Scotia, NB - New Brunswick, NL - Newfoundland & Labrador, YT - Yukon, NT - Northwest territories, PC - Parks Canada |
| NAT_PARK    | String  | Parks Canada National Parks ID |
| FIRE_ID     | String  | Agency fire ID |
| FIRENAME    | String  | Agency firename |
| LATITUDE    | Double  | Latitude of the fire point |
| LONGITUDE   | Double  | Longitude of the fire point |
| YEAR        | Integer | Year of fire as provided by individual agencies. -999 = unknown year; Some agency source data record their fires using fiscal year, however the NFDB 'year' field represents calendar year, derived from REP_DATE. |
| MONTH       | Integer | Month of fire as provided by individual agencies |
| DAY         | Integer | Day of fire as provided by individual agencies |
| REP_DATE    | Date    | Date associated with fire as reported by individual agency |
| ATTK_DATE   | Date    | No info |
| OUT_DATE    | Date    | No info |
| SIZE_HA     | Double  | Fire size (hectares) as reported by agency |
| CAUSE       | String  | General cause of fire as reported by agency. N-Natural/Lightning caused; H-Human caused; H-PB Human prescribed burn; U-Unknown/undetermined cause |
| CAUSE2      | String  | No info. Potentially the secondary cause of fire. |
| FIRE_TYPE   | String  | Fire type as indicated by source agency. There is currently no official national standard that has been applied to this attribute |
| RESPONSE    | String  | Response type. Standard classes include FUL-Full response, MOD-Modified response, MON-Monitored. Additional values may be used by some agencies, and over time |
| PROTZONE    | String  | Protection Zone as indicated by the source agency. There is currently no official national standard that has been applied to this attribute. |
| PRESCRIBED  | String  | No info. Potentially prescribed burn or not a prescribed burn. |
| MORE_INFO   | String  | Additional attributes provided by agency |
| CFS_NOTE1   | String  | Additional note added by CFS when compiling the NFDB. |
| CFS_NOTE2   | String  | Additional note added by CFS when compiling the NFDB. |
| ACQ_DATE    | Date    | Date that fire data was acquired from agency |
