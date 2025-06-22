# Haversine distance calculation using ckks homomrphic encryption

## Execution of the code

First after cloning repository setup environment

```
virtualenv .venv
```
\
Activate virtual environment 
```
source .venv/bin/activate
```
\
Install dependencies
```
pip install -r requirements.txt
```
\
Then to run tests execute:

```
python tests.py
```

`main.py` is uninportant at this moment but feel free to play around with it.

## Configuration of ckks context

Configuration of tenseal is in `tenseal_manager.py`. Most important parameters here are: 
* poly_modulus_degree
* coeff_mod_bit_sizes
* context.global_scale

Also important here is `"sqrt_c"` field in `consts` that defines coefficients used in approximating square root used  in `encrypted_functions.py`
