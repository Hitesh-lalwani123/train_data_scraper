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

    
### Phase 2
1. Try to get if travel gurantee provided that also take even if waitlisted.
2. Optimize the time taken to scrape data.
