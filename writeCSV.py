with open('StoredEmbedding.csv','a') as f:
    for i in range(512):
        f.write(str(i) + ",")