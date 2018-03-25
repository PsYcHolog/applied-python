def process(data, events, car):
    rezult_car=car
    for idx, event in enumerate(events):
        print("Новый ивент:")
        if event["type"] == "walk":
            # current info about passenger`s location
            current_car_name = get_train_info(pass_name=event['passenger'], trains=data)[0]
            current_car_index = get_train_info(pass_name=event['passenger'], trains=data)[1]
            current_train_name = get_train_info(pass_name=event['passenger'], trains=data)[2]
            # delete passenger from current car
            delete_pass_from_car(car_name=current_car_name, passanger=event['passenger'], trains=data)
            if current_car_index + event['distance'] < 0 or \
            current_car_index + event['distance'] > len(data[get_train_idx(train_name=current_train_name, trains=data)])-1:
                return -1
            # add passanger to car
            add_pass_to_car(passange=event['passenger'], car_index=current_car_index + event['distance'], train_name=current_train_name,  trains=data)
        else:
            switch_count=event['cars']
            # get trains indexes
            source_idx=get_train_idx(train_name=event['train_from'], trains=data)
            target_idx=get_train_idx(train_name=event['train_to'], trains=data)
            if len(data[source_idx]['cars']) >= switch_count:
                while switch_count > 0:
                    data[target_idx]['cars'].append(data[source_idx]['cars'][-1 * switch_count])
                    del data[source_idx]['cars'][-1*switch_count]
                    switch_count=switch_count-1
            else:
                return -1
    #return number of passangers in target car
    for train in data:
        for car in train['cars']:
            if car['name'] == rezult_car:
                return len(car['people'])

    for train in data:
        print(train['name'])
        for car in train['cars']:
            print('\t{}'.format(car['name']))
            for man in car['people']:
                print('\t\t{}'.format(man))
    print("Тест пройден. Запуск нового теста")
    return -1


def get_train_info(pass_name, trains):
    for train in trains:
        for idx, car in enumerate(train['cars']):
            for passanger in car['people']:
                if pass_name == passanger:
                    return car['name'], idx, train['name']
    return -1
 
def delete_pass_from_car(car_name, passanger, trains):
    for train in trains:
        for car in train["cars"]:
            if car['name'] == car_name:
                if passanger in car['people']:
                    car['people'].remove(passanger)
                    print("Passanger "+passanger+" Removed from car "+str(car_name))
                    return
    return -1

def get_train_idx(train_name, trains):
    for idx, train in enumerate(trains):
        if train['name'] == train_name:
            return idx
    return -1


def add_pass_to_car(passange, car_index, train_name, trains):
    for train in trains:
        if train_name==train['name']:
            for idx, car in enumerate(train["cars"]):
                if idx == car_index:
                    car['people'].append(passange)
                    print(passange+" Moves to car "+str(train['cars'][idx]))
                    return
    return -1