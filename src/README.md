## Source Code

There are two Python files: `run.py`, which runs the methods on the inputs, and `post-process.py`, which generates the final output files and posts the networks to GraphSpace.

### Dependencies

To generate the networks, users must:
1. Make an account on GraphSpace: [https://graphspace.org/](https://graphspace.org/). Your username will be your email; keep track of your password.
2. Install the `graphspace-python` module: see the [documentation](https://manual.graphspace.org/projects/graphspace-python/en/latest/) and [installation instructions](https://manual.graphspace.org/projects/graphspace-python/en/latest/Installing.html#installing).

If you do not want to generate networks, then you do not need to install any additional dependencies or make an account. However, you must comment out lines 1-2 from `post-process.py` (which imports the graphspace modules).

### `run.py``

```
USAGE: python run.py <INPUT_DIR> <OUTPUT_DIR>
```

This will generate files in the `OUTPUT_DIR` directory prefixed with `collapsed_` (which specifies that we are using the collapsed version of the interactome, which is the more recent version). An example run will look like:

```
python run.py ../inputs ../outputs
```

### `post-process.py`

```
USAGE: post-process.py <INPUT_DIR> <OUTPUT_DIR> <POST_NETS> <POST_FOCUS_NETS> <USERNAME> <PASSWORD>
	<INPUT_DIR> Directory of input files
	<OUTPUT_DIR> Directory of output files (outputs of run.py)
	<POST_NETS> (True/False) posts the method networks
	<POST_FOCUS_NETS> (True/False) posts the Oya network
	<USERNAME> GraphSpace Username (email address)
	<PASSWORD> GraphSpace Password
```

An example run without posting the networks will look like:

```
python post-process.py ../inputs ../outputs False False your_email your_graphspace_password
```
