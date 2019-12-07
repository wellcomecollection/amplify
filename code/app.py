import config
import parse_message
import google_vision_api


response = google_vision_api.detect_text(config.IMAGE_PATH[0])

print(response)

path = config.WORLDCAT_READ_API_RESPONSE_PATH[0]

parse_message.parse(path)


