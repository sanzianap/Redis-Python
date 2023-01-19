import redis as red
import datetime

redis = red.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

#la base de donnees
redis.hmset('user:prichicis@gmail.com', {'connexion':1, 'date0':'13:40'})
redis.hmset('user:prichicisanziana@gmail.com', {'connexion':3, 'date0':'13:40', 'date1':'14:40', 'date2':'18:40'})
redis.hmset('user:pl', {'connexion':8, 'date0':'21:23', 'date1':'23:34', 'date2':'23:34', 'date3':'23:34', 'date4':'23:34', 'date5':'23:34', 'date6':'23:34', 'date7':'23:34'})

#l'utlisateur introduit
new_user='user:prichicis@gmail.com'

#l'heure de la connexion
x = datetime.datetime.now()
ora=x.hour*60+x.minute

if redis.hexists(new_user,'connexion')==False:
    hour=str(x.hour)+':'+str(x.minute)
    redis.hmset(new_user, {'connexion':1, 'date0':hour})
else:
    y=int(redis.hget(new_user,'connexion'))
    #print("On a connexions", y)
    drop=-1
    for i in range(y):
        date='date'+str(i)
        if ora-(int(redis.hget(new_user,date)[0:2])*60+int(redis.hget(new_user,date)[3:5]))<10:
            drop=i
            break
    print(drop)
    #si drop== -1 => on doit effacer toutes les connexions car elles sont *expired* et on ecrit la connexion actuelle
    #si drop=0 et on a 10 connexions => on ne peut pas ecrire encore + message d'erreur
    #si drop=0 et on n'a pas 10 connexions => ajouter dans la position y
    #si drop!=0 => on doit effacer les connexions *expired* (qui on plus que 10 minutes) et on ecrit la connexion actuelle
    if drop==-1:
        for i in range(y):
            date='date'+str(i)
            redis.hdel(new_user, date)
        redis.hset(new_user, 'connexion', 1)
        redis.hset(new_user, 'date0', str(x.hour)+':'+str(x.minute))
    elif drop==0:
        if int(redis.hget(new_user,'connexion'))>=10: 
            print("no connexion available")
        else:
            date='date'+str(y)
            ora=str(x.hour)+':'+str(x.minute)
            y=y+1
            redis.hmset(new_user, {'connexion':y, date:ora})
    else:
        #print("la premiere connexion valide", drop)
        for i in range(y-drop):
            date_keep='date'+str(i)
            date_move='date'+str(drop+i)
            val=redis.hget(new_user,date_move)
            print(val[2:6])
            redis.hset(new_user, date_keep, str(val))
        for i in range(y-drop,y):
            date_drop='date'+str(i)
            redis.hdel(new_user,date_drop)
        redis.hset(new_user,'connexion', y-drop+1)
        redis.hset(new_user, 'date'+str(y-drop), str(x.hour)+':'+str(x.minute))
        
        
    
  
    


