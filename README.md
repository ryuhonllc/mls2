<head> <meta charset="UTF-8"></head>



This repo is for the second machine learning course of the TBDSG. This meetup session is being held jointly with the tampa bay python meetup. Thus, I've shuffled the material around a bit.

This session will focus on support tools for machine learning, plus a brief survey of how to use those tools.

Since this session has two target audiences, it will be difficult to address both. Try pairing up to share expertise.

```
  note: the links in this readme are intended to be executed from an jupyter notebook
```

# Support Tools

Perhaps more than other areas, machine learning environments have deep and often specific dependencies.  These can often conflict, so as a rule you should start with a virtual environment.  This session assumes you are doing so.

## git

You'll need git to get this repo.  Install that now if you don't already have it.

## python

I'm using python3 for this session. (yay) 

## virtual envs

python3 has a built in support via pyvenv, so you should not need to download additional scripts.  However, if you like other tools (eg mkvirtualenv) feel free to use them.

## pip

I've listed the dependencies in requirements.txt.  The step below will install those dependencies.  I'll talk more about them in the next few pages.


## Setup the environment

After you have the external dependecies installed, bootstrap the environment via these commands.

    git clone http://github.com/ryuhonllc/mls2
    cd mls2
    pyvenv .
    . bin/activate
    pip install -r requirements.txt
    pip install pymc


Don't worry too much about having multiple venvs.  pip caches stuff so you won't have to redownload, and disk space is cheap.

# The content

# Support Libraries

This section deal with stuff you can do inside python.

## numpy

numpy is essential. This session touches on:

* [numpy and speed](/notebooks/numpy/speed.ipynb)
* [numpy and brevity](/notebooks/numpy/vectorize.ipynb)

* To get actually fast code, you need numpy
* many libraries depend on it
    * pandas
    * scipy
* Many that don't, imitate it
    * tensor flow


## file management

### csv

There isn't much to say about csv.  Of course, there is the [standard csv library](https://docs.python.org/3/library/csv.html).
However, be aware that many technical libraries also support csv:

* [numpy via loadtxt](https://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html)
* [pandas via read_csv](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html)


### hd5f

If you've outgrown csv, where should you go next? hdf5 offers some great features.

[notebook comparing load speeds](/notebooks/hd5f/speed.ipynb)

### python!

Looking for speed? saving your data as python and then evaluating it to reload is actually pretty fast.

## command line arguments

make your code easier to run.  Start with `begins` and then add parameters as needed. Check out the low pass filter and animation example.

## ipython/jupyter notebook

I don't find this to be great for development, but it is great for sharing. Because many of these examples are in notebooks, I'm not covering this directly.

## visualization

### matplotlib

This is the de facto visualization tool for python, but you might outgrow it quickly depending on your requirements. It's still a good place to start.

[Matplotlib visualizations](/notebooks/visualization/matplotlib.ipynb)

### opencv

Even though it's for computer vision, opencv can be handy for visualizing your code, especially if you are working with images, of course.

The neural network video used opencv (along with ffmpeg) to generate visuals.

## brevify your code with unicode literals

The greek alphabet is all over machine learning. α is everywhere. However, we usually write 'alpha' in our code. Unfortunately, this often makes your equations too long for pep8. Increase readability by using greek symbols directly!

example:

        iota = a*(1 - alpha)^(beta*t) + aprime*(alpha)^(beta*t)
        # vs
        Φ = a*(1-α)^(β*t) + aprime*(α)^(β*t)


* this looks more like this equation in whatever paper you're using
* the code is shorter and easier to read

Most code editors make it easy to assign abbreviations. I suggest the LaTeX bindings (eg \alpha → α). Take a look at [greek.py](/files/greek.py) for some vim tricks.


# Machine Learning

Finally, machine learning.  Making use of the APIs in this section builds on the previous section.  You'll find this in your work as well.  Often, a majority of your work in say, optimization, will involve feeding the right data to the optimization function.


## Supervised learning

labeled data

### neural networks

* watch this video of a project I did in tensor flow

### decision trees

Neural networks are known for being hard to understand. Decision trees "make
sense". Random forest performance is often pretty good.


## Unsupervised learning

unlabeled data

* clustering
* pca
* feature discovery

[K-means](/edit/cluster/bpmgroup.py) can be useful without being complicated.
This example is in one dimension, but automated grouping speeds my work up.

### optimization

Arguably supervised if you consider the target equation a "label"

* hill climbing
* simulated annealing
* curve fitting

Here's an [example of optimizing a low pass filter](/edit/lp.py)

### reinforcement learning

Not well known (and not a great fit for these types)

* genetic algorithms
* [Q-Learning](/edit/pursuers/OneD.py)
* bonus: [monte carlo simulation]()
