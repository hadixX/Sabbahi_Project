from django.http import JsonResponse
from django.shortcuts import render
import pickle as pk
import pandas as pd

from sklearn.preprocessing import StandardScaler


def home(request):


    return render(request, "app1/landing_page.html", context={})


def index(request):
    df = pd.read_excel("media/PD_PRED_15_LAST.xlsx", sheet_name='Sheet1')
    pt = df.groupby('permit_type')['permit_type'].agg(['unique']).apply(list).to_dict()
    bt = df.groupby('building_type')['building_type'].agg(['unique']).apply(list).to_dict()

    t = df.groupby('type')['type'].agg(['unique']).apply(list).to_dict()

    context = {
        'ptlist': dict(enumerate(pt['unique'], 1)),
        'btlist': dict(enumerate(bt['unique'], 1)),

        'tlist': dict(enumerate(t['unique'], 1))
    }

    return render(request, "app1/index.html", context={'bigdata': context})


def motor(request):
    if request.method == 'POST':
        permit_type = request.POST['pt']
        building_type = request.POST['bt']

        types = request.POST['t']
        floors = int(request.POST['floors'])
        parking_num = int(request.POST['parking_num'])
        area = float(request.POST['area'])
        waste_amount = float(request.POST['waste_amount'])



        dataset = pd.read_excel("media/PD_PRED_15_LAST.xlsx", sheet_name='Sheet1')

        pr1 = pd.DataFrame([[floors, permit_type, building_type
                                , parking_num, area, types, waste_amount]]
                           , columns=['floors', 'permit_type', 'building_type'
                , 'parking_num', 'area', 'type', 'waste_amount'])

        df = [dataset, pr1]
        dataset = pd.concat(df)

        x = dataset[['floors', 'permit_type', 'building_type'
            , 'parking_num', 'area', 'type', 'waste_amount']]

        sc1 = StandardScaler()
        x['area'] = sc1.fit_transform(x[['area']])
        x['waste_amount'] = sc1.fit_transform(x[['waste_amount']])

        x = pd.get_dummies(x, columns=['permit_type',
                                       'building_type', 'type'])

        x_pred = x.iloc[[-1]].values

        regressor = pk.load(open('media/regressor.pkl', 'rb'))

        a = regressor.predict(x_pred)



        df = pd.read_excel("media/PD_PRED_15_LAST.xlsx", sheet_name='Sheet1')
        pt = df.groupby('permit_type')['permit_type'].agg(['unique']).apply(list).to_dict()
        bt = df.groupby('building_type')['building_type'].agg(['unique']).apply(list).to_dict()
        d = df.groupby('district')['district'].agg(['unique']).apply(list).to_dict()
        t = df.groupby('type')['type'].agg(['unique']).apply(list).to_dict()

        context = {
            'ptlist': dict(enumerate(pt['unique'], 1)),
            'btlist': dict(enumerate(bt['unique'], 1)),
            'dlist': dict(enumerate(d['unique'], 1)),
            'tlist': dict(enumerate(t['unique'], 1)),
            'feeAmount': round(a[0], 2)
        }

        return render(request, "app1/index.html", context={'bigdata': context})

    return render(request, "app1/index.html", context={})
