import random
import csv

bacteria = ["E.coli","Klebsiella","Pseudomonas"]
antibiotics = ["Ciprofloxacin","Amoxicillin","Ceftriaxone","Gentamicin","Meropenem","Imipenem"]
genders = ["Male","Female"]
results = ["R","S","I"]

with open("dataset.csv","w",newline="") as f:

    writer = csv.writer(f)

    writer.writerow(["age","gender","bacteria","antibiotic","result"])

    for i in range(1000):

        writer.writerow([
            random.randint(20,80),
            random.choice(genders),
            random.choice(bacteria),
            random.choice(antibiotics),
            random.choice(results)
        ])

print("Dataset created successfully")