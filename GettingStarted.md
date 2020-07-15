# Getting Started with turboCLOUD

This is a description of all of the files in the `turbo_cloud`: what they are and how to use them.  A good understanding of the functional significance of each "pipe" in the "pipeline" will give you a solid foundation of knowledge necessary to begin working with turboCLOUD.

For starters, let's begin with a high-level overview of the turboSETI data pipeline, the underlying framework that turboCLOUD simply makes cloud-compatible.  The pipeline can be thought of as 3 tasks:
1. Search
2. Find
3. Plot

In the next sections, we will make use of flow graphs to explain the what/how for each task.  Ultimately, the aim is to help you understand how data flows in turboSETI (i.e., expected I/O) and by extension, what the overall data flow of turboCLOUD will look like.

#### Note: The following will provide only a *high-level* overview of turboSETI.  For those interested in a more technical overview, refer to the turboSETI documentation and/or the Breakthrough Listen [data format paper](https://ui.adsabs.harvard.edu/abs/2019arXiv190607391L/abstract).

## Search
Here, we have a diagram that shows the initial input to turboSETI being a .h5 file.  [add more description]
<p align="center">
  <img src="https://github.com/rtraas/turboCLOUD/raw/master/Search-Flow-Diagram.png">
</p>

## Find
[add description]
<p align="center">
  <img src="https://github.com/rtraas/turboCLOUD/raw/master/Find-Flow-Diagram.png">
</p>


## Plot
[add description]
<p align="center">
  <img src="https://github.com/rtraas/turboCLOUD/raw/master/Plot-Flow-Diagram.png">
</p>
