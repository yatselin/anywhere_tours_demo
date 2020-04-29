from django.shortcuts import render
from django.views import View
import tours.data as data
from django.http import Http404
import random

# Constants
TOUR_NUMBER_PRESENTED = 6


# Add default data if needed
def populate_database(lst, cnt):
    while cnt < TOUR_NUMBER_PRESENTED:
        lst.append(data.default[-1])
        cnt += 1


# MIN and MAX calculation for Departure template
def min_max_count(data_id_selector, data_key):
    result = {"max": 0, "min": 999_999_999}
    for id in data_id_selector:
        if data.tours[id][data_key] > result["max"]:
            result["max"] = data.tours[id][data_key]
        if data.tours[id][data_key] < result["min"]:
            result["min"] = data.tours[id][data_key]
    return result


class MainView(View):
    def get(self, request, *args, **kwargs):
        # show random tours
        # retrieve required id's from data.py (database)
        data_id_selector = list()
        for id in data.tours.keys():
            data_id_selector.append(id)
        # choose tours to show randomly
        set_context = set()
        while len(set_context) < TOUR_NUMBER_PRESENTED:
            set_context.add(random.choice(data_id_selector))
        list_context = list()
        for id in set_context:
            list_context.append(data.tours[id])
        context = {"tour": list_context, "ids": list(set_context)}
        return render(request, 'index.html', context)


class DepartureView(View):
    def get(self, request, departure_city, *args, **kwargs):
        data_id_selector = list()
        cnt_id = 0
        for id in data.tours:
            if data.tours[id]["departure"] == departure_city:
                data_id_selector.append(id)
                cnt_id += 1
        list_context = list()
        for id in data_id_selector:
            list_context.append(data.tours[id])
        nights_num = min_max_count(data_id_selector, "nights")
        price_num = min_max_count(data_id_selector, "price")

        # Add default data if needed
        if cnt_id < TOUR_NUMBER_PRESENTED:
            populate_database(list_context, cnt_id)

        context = {
                    "tour": list_context,
                    "ids": data_id_selector,
                    "departure_city": data.departures[departure_city],
                    "tour_count": cnt_id,
                    "nights": nights_num,
                    "price": price_num
                }
        return render(request, 'departure.html', context)


class TourView(View):
    def get(self, request, id, *args, **kwargs):
        if id not in data.tours:
            raise Http404
        context = {
                "tour": data.tours[id],
                "departure_city": data.departures[data.tours[id]["departure"]]
                }
        return render(request, 'tour.html', context)
