import requests, os, dotenv
from typing import Any


# Load .dotenv file
dotenv.load_dotenv()
REPOSITORY   :str = os.getenv("REPOSITORY", "")
GITHUB_TOKEN :str = os.getenv("GITHUB_TOKEN", "")


def getImageIds(repo :str, token :str) -> list[int]:
    
    # Get all ids
    ids :list[int] = []

    # Request page
    page = 1
    while True:
        try:
            # Get all images
            resp :requests.Response = requests.get(
                url     = f"https://api.github.com/user/packages/container/{repo}/versions?page={page}&per_page=100",
                headers = {
                    "Authorization": f"Bearer {token}"
                },
                timeout = 10
            )
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        # Convert response to json
        respJson :list[dict[str, Any]] = resp.json()
        if not respJson: break

        for imageData in respJson:

            # Get tags for image
            tags :list[str] = imageData["metadata"]["container"]["tags"]
            # If tag list is empty, add to id list
            if not len(tags):
                ids.append(imageData["id"])
        
        # Check next page
        page += 1

    return ids


# Delete untagged images
def deleteUntaggedImages(repo :str, token :str, ids :list[int]):
    
    for imageId in ids:
        try:
            requests.delete(
                url     = f"https://api.github.com/user/packages/container/{repo}/versions/{imageId}",
                headers = {
                    "Authorization": f"Bearer {token}"
                }
            )
        except requests.exceptions.RequestException as e:
            print(f"Error while deleting image with id: {imageId}")

    return


if __name__ == '__main__':

    # Get all images without tags
    ids :list[int] = getImageIds(REPOSITORY, GITHUB_TOKEN)

    # Print log
    idsStrings :list[str] = [str(id) for id in ids]
    print(f"Images with following ids will be deleted from repository '{REPOSITORY}': [{', '.join(idsStrings)}]")
    print(len(idsStrings))

    # Delete all images from response above
    deleteUntaggedImages(REPOSITORY, GITHUB_TOKEN, ids)

    # Print log
    print("Finished deleting ids, exiting program...")

    exit(0)