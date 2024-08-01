status = "Watching"
# Add - On-Hold, Remove - Watching

text = """"""

ids = set([x.strip("https://myanimelist.net/anime/") for x in text.split("\n")])


print("""<?xml version="1.0" encoding="UTF-8" ?>
                <!--
                 Created by XML Export feature at MyAnimeList.net
                 Version 1.1.0
                -->

                <myanimelist>

                        <myinfo>
				<user_id>1</user_id>
				<user_name>test</user_name>
				<user_export_type>1</user_export_type>
				<user_total_anime>0</user_total_anime>
				<user_total_watching>0</user_total_watching>
				<user_total_completed>0</user_total_completed>
				<user_total_onhold>0</user_total_onhold>
				<user_total_dropped>0</user_total_dropped>
				<user_total_plantowatch>0</user_total_plantowatch>
                        </myinfo>""")
for i in set(ids):
    print("""				<anime>
					<series_animedb_id>{}</series_animedb_id>
					<my_status>{}</my_status>
					<update_on_import>1</update_on_import>
				</anime>
""".format(i, status))
    
print("		</myanimelist>")
input()