import csv
import numpy as np
import operator
import read

def init_model(vec_len):
    return np.random.randn(vec_len)

def moodel_predict(user_vec,movie_vec):
    res = np.dot(user_vec, movie_vec)/(np.linalg.norm(user_vec)*np.linalg.norm(movie_vec))
    return res

def lfm_train(train_data,F,alpha,beta,step):
    user_vec = {}
    movie_vec = {}
    for step_index in range(step):
        for data_instance in train_data:
            userid,movieid,label = data_instance
            if userid not in user_vec:
                user_vec[userid] = init_model(F)
            if movieid not in movie_vec:
                movie_vec[movieid] = init_model(F)
        delta = label - moodel_predict(user_vec[userid], movie_vec[movieid])
        for index in range(F):
            user_vec[userid][index] += beta*(delta*movie_vec[movieid][index]-alpha*user_vec[userid][index])
            movie_vec[movieid][index] += beta*(delta*user_vec[userid][index]-alpha*movie_vec[movieid][index])
        beta = beta*0.9
    return user_vec, movie_vec


def give_recom_result(user_vec,movie_vec,userid):
    fix_num = 10
    if userid not in user_vec:
        return []
    record = {}
    recom_list = []
    user_vector = user_vec[userid]
    for movieid in movie_vec:
        movie_vecor = movie_vec[movieid]
        res = np.dot(user_vector, movie_vecor)/(np.linalg.norm(user_vector)*np.linalg.norm(movie_vecor))
        record[movieid] = res
    for allpairs in sorted(record.items(),key=operator.itemgetter(1), reverse=True)[:fix_num]:
        movieid = allpairs[0]
        score = round(allpairs[1], 3)
        temp=[userid,movieid]
        recom_list.append(temp)
    return recom_list



def train_model_process():
    train_data = read.get_train_data('C:\\Users\zou\Desktop\LFM--main\\ratings.txt')
    user_vec, movie_vec = lfm_train(train_data, 50, 0.01, 0.1, 50)
    with open('C:\\Users\zou\Desktop\LFM--main\movie.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for userid in user_vec:
            res = give_recom_result(user_vec, movie_vec, userid)
            for row in res:
                writer.writerow(row)

if __name__ == '__main__':
    train_model_process()


