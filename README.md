

# Computer Vision : Using Satellite images to Predict Economic Indicators

## Getting Started

### Literature Review

- [A Primer on Remote Sensing For Economists](https://olc.worldbank.org/system/files/Primer_Satellite%20Data_Econ.pdf)
  - Social scientists almost never use raw satellite data.
  - Extensive processing is typically required to make data comparable and interpretable, and there is
an active remote sensing literature developing and refining these methods and
applying them to new and existing datasets.
  - In remote sensing parlance, raw data are called Level 0 data, while data providers often release Level 1 or Level 2 data,
  - **Interpretation**
      - While some applications discussed below involve relatively direct conversion of sensed quantities for individual pixels to physical quantities of interest (such as night lights, greenness, elevation, particulate concentration, or temperature), many others instead involve classifying pixels, each of which is a vector of quantities in different bands, into a discrete set of land cover categories.
      - Sophisticated supervised classification systems increasingly rely on machine learning techniques. A critical input to these and other methods is the availability of training data on the variable of interest that assigns ground truth values to sample
sites. For example, delineating imaged urban neighborhoods as residential, or even more specifically as slums, requires first providing a set of areas pre-defined as slums by other means. Doing so well requires a training dataset that reflects the full diversity of distinct neighborhoods within the category of slums. This is especially challenging when the object of interest is heterogeneous or imprecisely defined.

- *Expensive Land Surveys*
  -  These surveys have limited repeated observation of individual locations, making it
difficult to measure local changes in well-being over time, and public release of any disaggregated consumption data from
African countries is very rare. At current survey frequencies, we calculate that a given African household will appear in a household well-being survey less than once every 1000 years, or about two orders of magnitude less frequently than a household in the United States (Fig. 1b). While not all households need to be observed to generate accurate economic estimates, sampling enough households to generate frequent and reliable national level statistics is alone likely to be expensive, requiring an estimated $1 billion USD annual investment in lower-income countries to measure a range of indicators relevant to the Sustainable Development Goals6. Expanding these efforts to generate reliable estimates at the local level would add dramatically to these costs.
  - ![image](https://user-images.githubusercontent.com/6872080/96285510-0e621580-0fad-11eb-8afa-5b970834d539.png)
    - [Source : Yeh, Perez Et al](https://www.nature.com/articles/s41467-020-16185-w.pdf)


## Project Flow

![image](https://user-images.githubusercontent.com/6872080/96283614-77945980-0faa-11eb-8ac4-d1333c633f8b.png)


## Geoprocessing In Python

- [Overview](https://carpentries-incubator.github.io/geospatial-python/aio/index.html)

* Earh py errors
- install depenedencies individually using PIP
- https://github.com/azavea/raster-vision/issues/518
- https://www.lfd.uci.edu/~gohlke/pythonlibs/#rasterio
