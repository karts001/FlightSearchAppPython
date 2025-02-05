class Conversions:

    def convert_iso_time_to_minutes(self, duration: str):
        # api response returns time in iso string format
        # need to convert this string into number of minutes
        # string is in this format: PTxxHyyM
        # two edge cases where flight duration is only minutes or hours

        no_pt = duration.split("PT")[1]
        no_m = no_pt.split("M")[0]
        time = no_m.split("H")

        
        if "" in time:
            hours = time[0]
            
            return int(hours)   
        else:
            hours = time[0]
            minutes = time[1]

            return (int(hours) * 60) + (int(minutes))
        
