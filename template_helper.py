import cv2
import numpy as np
import argparse
import json


def generate_template_json(template_file_name):
    template_img = cv2.imread(template_file_name)
    (height,width,channels) = template_img.shape
    instruction_img = np.zeros((height,int(width/3),channels), np.uint8)
    instructions = [["Please click to select","1. Course name start"],
                    ["Please click to select","2. Course name end"],
                    ["Please click to select","3. Student name start"],
                    ["Please click to select","4. Student name end"],
                    ["Please click to select","5. Date start"],
                    ["Please click to select","6. Date end"],
                    ["Please click to select","7. Sign start"],
                    ["Please click to select","8. Sign end"],
                    ["Press any key to exit"," "]]

    font = cv2.FONT_HERSHEY_PLAIN
    # Black color in BGR
    color = (255, 0, 0)
    scale = 1
    thickness = 1
    x_coord = width + 5
    y_coord = 25

    combined_image = np.hstack((template_img,instruction_img))

    field_list = ["course_name_start","course_name_end","student_name_start","student_name_end",
            "date_start","date_end", "sign_start","sign_end"]
    field_count = 0
    field_dict = dict()
    window_name ="Template Helper"

    print(f"Please click to select {field_list[field_count]} coordinates")


    def click_event(event, x, y, flags, params):
        nonlocal field_list
        nonlocal field_count
        nonlocal instructions
        if event == cv2.EVENT_LBUTTONDOWN:
            if field_count < len(field_list):
                field_dict[field_list[field_count]] = (x,y)
                print(f"Selected ({x},{y}) for {field_list[field_count]}")
                field_count += 1
                temp_image = combined_image.copy()
                y_coord = 25
                temp_image = cv2.putText(temp_image, instructions[field_count][0],
                (x_coord,y_coord), font,scale, color, thickness, cv2.LINE_AA)
                y_coord = 50
                temp_image = cv2.putText(temp_image, instructions[field_count][1],
                (x_coord,y_coord), font,scale, color, thickness, cv2.LINE_AA)
                cv2.imshow(window_name,temp_image)

                if field_count < len(field_list):
                    print(f"Please click to select {field_list[field_count]} coordinates")

    temp_image = combined_image.copy()

    temp_image = cv2.putText(temp_image, instructions[0][0],(x_coord,y_coord), font,scale, color, thickness, cv2.LINE_AA)
    y_coord += 25
    temp_image = cv2.putText(temp_image, instructions[0][1],(x_coord,y_coord), font,scale, color, thickness, cv2.LINE_AA)

    cv2.imshow(window_name,temp_image)
    cv2.setMouseCallback(window_name, click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    template_json_file = '.'.join(template_file_name.split('.')[:-1] + ['json'])
    with open(template_json_file,"w") as f:
        json.dump(field_dict,f)


def main(args):
    if args.verbose:
        print('Arguments passed',args)
    generate_template_json(args.template_file_name)



if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("template_file_name",type=str, help="Template file name")

    parser.add_argument("-v", "--verbose", action="store_true", default=False,help= "Whether vebose message are required. (Default: %(default)r)")

    args = parser.parse_args()
    main(args)