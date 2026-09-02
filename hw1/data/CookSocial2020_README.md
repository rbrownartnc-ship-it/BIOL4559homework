# CookSocial2020

This is a dataset of behavioral data collected from beetles at the Mountain Lake Biological Station between 2018 and 2020. There are 12 condos, each containing a population of 36 beetles, labeled 1A, 1B,...,6A, 6B. The data are collected 3 times per day.

In each condo, there is a wall simulating a natural environment, gridded up into a 3 row, 18 column grid, some of have fungus brackets. Rows are labeled A, B, and C and columns are labeled 1 through 18.

The data format is in CSV, with the following fields:
* datetime: The date and time at which the observation was made in UTC format
* condo: a two-character code representing the mesocosm for the experimental networks
* focal_id: The beetle being observed (If unknown, the ID is UKM, UKF, or UK)
* sex: the sex of the focal beetle [M or F (or UK for unknown)]
* behavior: the behavior of the focal beetle (S: stationary, M: moving)
    * S = stationary
	* M = moving
	* CRT/MCRT/FCRT = courting
	* COP = copulating
	* G = mate-guarding
	* F = fighting
	* L = laying an egg
	* OS = ovipositor out, searching for an oviposition site
* grid_cell: the location of the individual within the gridded artificial log (A01-C18) or elsewhere in the mesocosm
    * AS = above the artificial log
	* US = under the artificial log
	* M = in the mulch
	* W = on one of the walls
	* Leg = one of the supports of the artificial log
	* Back = on the back of the artificial log
* cell_location: the location in the grid cell
    * T = on top of a fungus bracket
	* B = on the bottom of a fungus bracket
	* E = on the edge of a fungus bracket
	* I = buried inside a fungus bracket
	* C = elsewhere in the cell
* partner_id: The ID of a partner beetle interacting with the focal beetle.
* partner_interaction: The type of interaction the two beetles are engaged in. Either proximity, touch, or mating.

## Excerpts from original dataset information

1. Title of Dataset: Social network and fitness data from age-structured populations of forked fungus beetles 

2. First/Corresponding Author Contact Information:
	Name: Phoebe A. Cook
	Institution: University of Virginia
	Address: Department of Biology
	Email: pac6he@virginia.edu

The authors welcome any questions about methods or requests for resources not included here. 

3. Date of data collection (single date, range, approximate date): July-August 2020

4. Geographic location of data collection: Near Mountain Lake Biological Station, Pembroke, Virginia, United States

5. Information about funding sources that supported the collection of the data: 
This work was supported by the National Science Foundation and the University of Virginia.

METHODOLOGICAL INFORMATION

1. Description of methods used for collection/generation of data: 
We established a captive breeding population of B. cornutus at Mountain Lake Biological Station (37°22'37.0"N, 80°31'17.5"W), founded with wild beetles collected from the surrounding area in autumn 2017 and spring 2018. We created twelve experimental populations of thirty-six beetles each and surveyed their social interactions for three weeks for a different research project in the summer of 2018 (Costello et al. 2022a, 2022b). Although the exact age of these wild-caught founders is unknown, we know their minimum age from their time of capture. Several years of field surveys of a nearby metapopulation have found that 60% of all observations are of individuals not observed in previous years (Formica and Brodie, unpublished data), so this minimum is likely correct for the majority of individuals and conservative for the rest. For the next two years we allowed all beetles to breed and deposit eggs on fungus brackets in screen enclosures exposed to natural abiotic conditions. Adults were shuffled among enclosures to mimic natural migration and promote genetic diversity. Offspring developed inside the old fungus brackets until emergence, just as in the wild. Each year we searched the populations for newly emerged offspring and marked them with a unique three-character code affixed to their elytra with a UV-cured acrylic epoxy (Tuffleye Wet-A-Hook Technologies, San Antonio, TX). Beetles captured as adults in early spring were assumed to have emerged late in the previous year, and to therefore be one year old. 
By late summer 2020, we had three age cohorts: young-of-the-year (hereafter “first-year” adults) newly emerged earlier that summer, two-year-olds first caught in spring of 2019, or wild-caught in 2017 and spring 2018 and therefore at least three years old. Note that we are excluding one-year-olds, meaning beetles who had emerged in fall of 2019 and overwintered, because sampling was not possible during early spring 2020 due to pandemic constraints.
In August of 2020, we tested the effects of both individual and social group age on behavior by creating two different experimental treatments. We replicated our methodology from 2018 to created twelve experimental populations of thirty-six beetles each, but this time with six replicates in both of two treatments. The six “young” populations consisted of eighteen first-years and eighteen two-year-olds, and the six “old” populations consisted of eighteen two-year-olds and eighteen beetles that were three (or more) years old. These compositions approximate two ends of the range in age structure observed in natural populations. 
We minimized differences among these populations in sex ratio, body size, relatedness, and past interaction history. The body size of each individual was measured as the length of the elytra from an image taken on a flatbed scanner (Epson Perfection V600 Photo) using ImageJ (Abramoff et al. 2003). We then used structured sampling from sex- and age- specific size quantiles to create populations that had equal sex ratios and did not differ from each other in body size (F11,402 = 0.21, p = 0.997) (see Cook et al. 2022 Supplemental Material for details). This process was repeatedly simulated until the population assignments also minimized the number of beetles placed together who had overwintered or emerged from the same enclosure. All were held in isolation for at least seven days before the start of the experiment, which past studies suggest is enough time for patterns of social interaction to “reset” (Formica et al. 2017). 
In both 2018 and 2020, populations interacted freely within 2.4 by 2.4 by 1.2 m screened experimental enclosures built to mimic natural resource patches in the forest. Enclosures contained mulch floors and “artificial logs,” wooden shelving units holding 54 bags of hardwood sawdust. Eighteen of those bags were inoculated with the same strain of the B. cornutus host fungus species Ganoderma tsugae (Sharondale Mushroom Farm), a B. cornutus host species, and allowed to produce brackets. These shelves mimic the logs on which beetles live in the wild, but with fungus age, size, genotype, and spacing all controlled so as not to vary between populations (see Costello et al. 2022b for details). Population densities were within the range observed in wild populations (Conner 1989b). The screened enclosures were placed in an area of forest where this species naturally occurs and were exposed to natural abiotic conditions. At the start of the experiment, individuals were allowed to acclimatize to the enclosures for 36 hours before behavioral observation began. After acclimatization, we performed scan sampling of all activity and dyadic interactions three times a day (0630-0930, 1430-1630, and 2130-0030) for 21 days. Any beetles that were visible to observers had emerged onto an exposed surface and were considered active; beetles that were not visible to observers were assumed to be sheltering within fungus brackets or tight crevices, with very little space for locomotion or social interaction. Individuals were defined as social partners if they were in physical contact or close proximity (within 5 cm) of one another, following past work in this system (Formica et al. 2012). Courtship and mating interactions were excluded because they are not included in measures of sociability (Gartland et al. 2021).
Both the order in which the populations were surveyed and individual observer identity were randomized to control for possible time and observer biases. Observers in 2020 could not be made fully blind to the age composition treatment because the individual identification codes used to label beetles have progressed in a predictable sequence over the years. However, the majority of the observers were not aware of the questions that would be answered with the data, and a priori predictions as to the direction of effects had not been made when data collection was underway. 

5. Environmental/experimental conditions: Natural variation in weather and temperature.  

6. Describe any quality-assurance procedures performed on the data: Extensive checking for possible observation or entry errors or low-certainty observations, which were corrected or removed in R. Contact the authors for full data clean-up script if needed. 

7. People involved with sample collection, processing, analysis and/or submission: 
Malcolm Augat, Fisher Brodie, Eileen Butterfield, Catherine Debban, Tom McNamara, and Liza Mitchem helped build experimental enclosures. Christine Alencar and Eileen Butterfield developed fungus-growing protocols, and Eileen Butterfield and Savanna Cabrera grew Ganoderma tsugae. Eileen Butterfield, Sylvie Finn, Lily Fornof, Kane Lawhorn, and Lisa Robbins helped collect beetles in 2017 and 2018. Rachel Thoms helped perform behavioral observations and enter and error check the 2018 data. Savanna Cabrera, Hannah Donald, and Sarah McPeek helped with 2020 data collection; Savanna Cabrera and Ahema Gaisie entered 2020 data; and Alejandro Medina-Valencia helped with 2020 data cleanup. Hannah Donald provided support with beetle size measurements, beetle labeling, data collection, and data management in all years, and Jaime Jones and Tom McNamara provided logistical support at Mountain Lake Biological Station.

DATA-SPECIFIC INFORMATION FOR: all_raw_behavioural_data.csv

NOTE: This file contains all behavioral data collected from the mesocosm populations. It was error-checked in both 2018 and 2019 but at this point the 2020 data were still raw and contained errors. 

1. Number of variables: 34

2. Number of cases/rows: 75,767

RecordNumber - a unique numerical value assigned by entry into the database
Date Started - the date, in format yyyymmdd, the survey began
Date_Surveys - the date, in format yyyymmdd, the data point was collected; this may be different than Date_Surveys when data collection goes past midnight 
Trial ID - a letter code indicating the time of day of the survey
	A = morning
	B = afternoon
	C = night
ScanID - a concatenation of Date Started and Trial ID to create a unique code for each survey
Time - the time of day, in 24hr time
Condo - a two-character code representing the mesocosm for the experimental networks 	
fkfieldID_surveys - a three-character code identifying each individual beetle, equivalent to the variable "Focal" in processed datasets
Survey_Sex - a character indicating the sex recorded in the field
	F = female
	M = male
	UK = unknown
Behavior - a character or string indicating the behavior recorded in the field
	S = stationary
	M = moving
	CRT/MCRT/FCRT = courting
	COP = copulating
	G = mate-guarding
	F = fighting
	L = laying an egg
	OS = ovipositor out, searching for an oviposition site
Secondary_Behavior - a character or string indicating another behavior, if applicable
Grid_Cell - the location of the individual within the gridded artificial log (A01-C18) or elsewhere in the mesocosm (AS = above the artificial log, US = under the artificial log, M = in the mulch, W = on one of the walls, Leg = one of the supports of the artificial log, Back = on the back of the artificial log)
Location - a character indicating where within the the grid cell the individual was: T = on top of a fungus bracket, B = on the bottom of a fungus bracket, E = on the edge of a fungus bracket, I = buried inside a fungus bracket, C = elsewhere in the cell
Partner	- a three-character code identifying a beetle with whom the focal individual was interacting
PartnerInteraction - a string describing whether the interaction was proximity, touch, or mating
