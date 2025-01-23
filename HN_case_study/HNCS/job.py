from.models import *
import requests
from datetime import datetime
def Store_News_every_five_minutes():
    syncval_obj = SyncVal.objects.first()
    syncval = syncval_obj.value
   
    getmaxitemid = f"https://hacker-news.firebaseio.com/v0/maxitem.json?print=pretty"
    response = requests.get(getmaxitemid)

    if response.status_code == 200:
        max_item_id = response.json()
        highest_id = max_item_id
    # Step 3: Calculate the current ID to fetch
    highest_id = int(highest_id) - 1
    current_id = highest_id
    if current_id <= 0:
        print("All records have been synced.")
        return

    # Step 4: Fetch the data from the API
    api_url = f"https://hacker-news.firebaseio.com/v0/item/{current_id}.json?print=pretty"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        Kids = []
        Parts =[]
        if data.get("type"):
            type=data.get("type")
        else:
            return
        if type == "comment":
            return
        dead = data.get("dead", False)
        deleted = data.get("deleted", False)
        # if type == "comment":
        #     chk_comment = Comment.objects.filter(comment_id=data.get("id")).first()
        #     if not chk_comment and dead == False and deleted ==False:
        #         Kids = data.get("kids", [])
        #         comment = Comment(
        #             comment_id=data.get("id"),
        #             by=data.get("by"),
        #             kids = [int(kid) for kid in Kids if isinstance(kid, int)],
        #             parent=data.get("parent"),
        #             text=data.get("text"),
        #             dead = data.get("dead", False),
        #             deleted = data.get("deleted", False),
        #             time=datetime.fromtimestamp(data.get("time")),
        #             type=data.get("type")
                    
        #         )
        #         comment.save()
        #         print(f"Record {current_id} saved successfully.")
        #         syncval_obj.value = syncval_obj.value + 1
        if type == "story":
            chk_story = Story.objects.filter(story_id=data.get("id")).first()
            if not chk_story and dead == False and deleted ==False:
                Kids = data.get("kids", [])
                story = Story(
                    story_id=data.get("id"),
                    by=data.get("by"),
                    descendants=data.get("descendants"),
                    # Ensure it's a list of integers
                    kids = [int(kid) for kid in Kids if isinstance(kid, int)],
                    score=data.get("score"),
                    title=data.get("title"),
                    type=data.get("type"),
                    url=data.get("url"),
                    time=datetime.fromtimestamp(data.get("time")),
                    dead = data.get("dead", False),
                    deleted = data.get("deleted", False)
                )
                story.save()
                print(f"Record {current_id} saved successfully.")
                syncval_obj.value = syncval_obj.value + 1
                print("story")
        elif type == "job":
            chk_job = Job.objects.filter(job_id=data.get("id")).first()
            if not chk_job and dead == False and deleted ==False:
                job = Job(
                    job_id=data.get("id"),
                    by=data.get("by"),
                    score=data.get("score"),
                    text=data.get("text"),
                    title=data.get("title"),
                    type=data.get("type"),
                    url=data.get("url"),
                    time=datetime.fromtimestamp(data.get("time")),
                    dead = data.get("dead", False),
                    deleted = data.get("deleted", False)
                )
                job.save()
                print(f"Record {current_id} saved successfully.")
                syncval_obj.value = syncval_obj.value + 1
                print("job")
        elif type == "poll":
            chk_poll = Poll.objects.filter(poll_id=data.get("id")).first()
            if not chk_poll and dead == False and deleted ==False:
                Parts = data.get("parts", [])
                Kids = data.get("kids", [])
                poll = Poll(
                    poll_id=data.get("id"),
                    by=data.get("by"),
                    descendants=data.get("descendants"),
                    parts = [int(part) for part in Parts if isinstance(part, int)],
                    kids = [int(kid) for kid in Kids if isinstance(kid, int)],
                    score=data.get("score"),
                    text=data.get("text"),
                    title=data.get("title"),
                    type=data.get("type"),
                    time=datetime.fromtimestamp(data.get("time")),
                    dead = data.get("dead", False),
                    deleted = data.get("deleted", False)
                )
                poll.save()
                print(f"Record {current_id} saved successfully.")
                syncval_obj.value = syncval_obj.value + 1
                print("poll")
        # elif type == "pollopt":
        #     chk_pollopt = Pollopt.objects.filter(pollopt_id=data.get("id")).first()
        #     if not chk_pollopt and dead == False and deleted ==False:
        #         pollopt = Pollopt(
        #             pollopt_id=data.get("id"),
        #             by=data.get("by"),
        #             poll=data.get("poll"),
        #             score=data.get("score"),
        #             text=data.get("text"),
        #             title=data.get("title"),
        #             type=data.get("type"),
        #             time=datetime.fromtimestamp(data.get("time")),
        #             dead = data.get("dead", False),
        #             deleted = data.get("deleted", False)
        #         )
        #         pollopt.save()
        #         print(f"Record {current_id} saved successfully.")
        #         syncval_obj.value = syncval_obj.value + 1
        #         print("pollopt")
            
    
       # Step 6: Update the sync value
        syncval_obj.save()
    else:
        print(f"Failed to fetch data for ID {current_id}. HTTP Status: {response.status_code}")
