#! /bin/bash

# python perona_malik.py --input=cameraman.jpg --dt=0.01 --K=20 --num_iteration=100 --interpolation=True
# python perona_malik.py --input=cameraman.jpg --dt=0.1 --K=20 --num_iteration=100 --interpolation=True
# python perona_malik.py --input=cameraman.jpg --dt=0.25 --K=20 --num_iteration=100 --interpolation=True
# python perona_malik.py --input=cameraman.jpg --dt=4 --K=20 --num_iteration=100 --interpolation=True

# python perona_malik.py --input=fingerprint-small.jpg --dt=0.01 --K=20 --num_iteration=100 --interpolation=True
# python perona_malik.py --input=fingerprint-small.jpg --dt=0.1 --K=20 --num_iteration=100 --interpolation=True
# python perona_malik.py --input=fingerprint-small.jpg --dt=0.25 --K=20 --num_iteration=100 --interpolation=True
# python perona_malik.py --input=fingerprint-small.jpg --dt=4 --K=20 --num_iteration=100 --interpolation=True

# python perona_malik.py --input=oyster-s1.jpg --dt=0.01 --K=20 --num_iteration=100 --interpolation=True
# python perona_malik.py --input=oyster-s1.jpg --dt=0.1 --K=20 --num_iteration=100 --interpolation=True
# python perona_malik.py --input=oyster-s1.jpg --dt=0.25 --K=20 --num_iteration=100 --interpolation=True
# python perona_malik.py --input=oyster-s1.jpg --dt=4 --K=20 --num_iteration=100 --interpolation=True

# python perona_malik.py --input=synpic45657.jpg --dt=0.01 --K=20 --num_iteration=100 --interpolation=True
# python perona_malik.py --input=synpic45657.jpg --dt=0.1 --K=20 --num_iteration=100 --interpolation=True
# python perona_malik.py --input=synpic45657.jpg --dt=0.25 --K=20 --num_iteration=100 --interpolation=True
# python perona_malik.py --input=synpic45657.jpg --dt=4 --K=20 --num_iteration=100 --interpolation=True


# hypertuning for K
# python perona_malik.py --input=cameraman.jpg --dt=0.25 --K=1 --num_iteration=100 
# python perona_malik.py --input=cameraman.jpg --dt=0.25 --K=25 --num_iteration=100
# python perona_malik.py --input=cameraman.jpg --dt=0.25 --K=50 --num_iteration=100 
# python perona_malik.py --input=cameraman.jpg --dt=0.25 --K=100 --num_iteration=100 

# # using tukey
# python perona_malik.py --input=cameraman.jpg --dt=0.01 --K=20 --num_iteration=100  --g_function=tukey
# python perona_malik.py --input=cameraman.jpg --dt=0.1 --K=20 --num_iteration=100  --g_function=tukey
# python perona_malik.py --input=cameraman.jpg --dt=0.25 --K=20 --num_iteration=100  --g_function=tukey
# python perona_malik.py --input=cameraman.jpg --dt=0.5 --K=20 --num_iteration=100  --g_function=tukey

# hypertuning for alpha in lorentz
python perona_malik.py --input=cameraman.jpg --dt=0.25 --K=20 --num_iteration=100  --g_function=lorentz --alpha=0.5
python perona_malik.py --input=cameraman.jpg --dt=0.25 --K=20 --num_iteration=100  --g_function=lorentz --alpha=1
python perona_malik.py --input=cameraman.jpg --dt=0.25 --K=20 --num_iteration=100  --g_function=lorentz --alpha=2
python perona_malik.py --input=cameraman.jpg --dt=0.25 --K=20 --num_iteration=100  --g_function=lorentz --alpha=4