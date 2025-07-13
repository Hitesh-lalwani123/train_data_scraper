### Phase 1
1. Extract all fields and push to db in format:
    ```{date: {
        train1: {
            'searched_station1-searched_station2,actual_station1-actual_station2':{
                'sl':['wl 2','rs233'],
                '3a':['wl 2','rs233'],
                '2a':['wl 2','rs233']
            },
            'searched_station1-searched_station3,actual_station1-actual_station3':{
                'sl':['wl 2','rs233'],
                '3a':['wl 2','rs233'],
                '2a':['wl 2','rs233']
            }
        },
        train2: {
            'searched_station1-searched_station2,actual_station1-actual_station2':{
                'sl':['wl 2','rs233'],
                '3a':['wl 2','rs233'],
                '2a':['wl 2','rs233']
            },
            'searched_station1-searched_station3,actual_station1-actual_station3':{
                'sl':['wl 2','rs233'],
                '3a':['wl 2','rs233'],
                '2a':['wl 2','rs233']
            }
        },
    }}```

2. convert get-progress api to get (currently post) and deploy it on render.
3. Change api's route to "api/v1/api-name"
    
### Phase 2
1. Try to get if travel gurantee provided that also take even if waitlisted.
2. Optimize the time taken to scrape data.
3. Update db progress (currently using first delete progress and then insert new -> update to update query instead of delete and then insert)
