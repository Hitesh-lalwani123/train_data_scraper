<!-- phase 1 -->
1. Extract all fields and push to db in format:
    {date: {
        train1: {
            'station1-station2':{
                'sl':['wl 2','rs233'],
                '3a':['wl 2','rs233'],
                '2a':['wl 2','rs233']
            },
            'station1-station3':{
                'sl':['wl 2','rs233'],
                '3a':['wl 2','rs233'],
                '2a':['wl 2','rs233']
            }
        },
        train2: {
            'station1-station2':{
                'sl':['wl 2','rs233'],
                '3a':['wl 2','rs233'],
                '2a':['wl 2','rs233']
            },
            'station1-station3':{
                'sl':['wl 2','rs233'],
                '3a':['wl 2','rs233'],
                '2a':['wl 2','rs233']
            }
        }
    }}

    
<!-- phase 2 -->
try to get if travel gurantee provided that also take even if wl
