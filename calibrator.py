def calibrate():
    import cv2 as cv
    from phonebot import PhoneBot
    
    x1, x2, y1, y2 = 145, 180, 150, 220

    bot = PhoneBot()
    bot.connect()
    bot.home()

    bot.move_to(x=x1,y=y1)
    bot.tap()

    bot.move_to(x=x1,y=y2)
    bot.tap()

    bot.move_to(x=x2, y=y2)
    bot.tap()

    bot.move_to(x=x2, y=y1)
    bot.tap()

    bot.move_to(x=25, y=200)
    cap = cv.VideoCapture(-1)
    while True:
        ret, frame = cap.read()

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray = cv.bilateralFilter(gray,7,75,75)

        #threshed = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
        ret,threshed = cv.threshold(gray,120,255,cv.THRESH_BINARY)
        
        contours, hierarchy = cv.findContours(threshed, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        colored = cv.cvtColor(gray,cv.COLOR_GRAY2RGB) 
        cv.drawContours(colored, contours, -1, (0,255,0), 3)
        print("*****")
        points = []
        if len(contours) == 5:
            for contour in contours:
                bx, by, bw, bh = cv.boundingRect(contour)
                if bh > 200:
                    screen_x = bx
                    screen_y = by
                    screen_w = bw
                    screen_h = bh
                else:
                    points.append((bw/2+bx, bh/2+by))
        
        cv.imshow('image', colored)
        
        if points:
            points.sort(key = lambda x: x[0])
            #sort by the x values. Then average the first and second. Then the second and third
            x_min = (points[0][0] + points[1][0]) // 2
            x_max = (points[2][0] + points[3][0]) // 2
            
            points.sort(key = lambda x: x[1])
            y_min = (points[0][1] + points[1][1]) // 2
            y_max = (points[2][1] + points[3][1]) // 2
          
            with open("calibration_constants.txt", "w") as f:
                f.write("{}, {}, {}, {}, {}, {}, {}, {}".format(x1, x2, y2, y1, int(x_min), int(x_max), int(y_min), int(y_max)))
                    
        if cv.waitKey(1) == ord('q'):
            break

def camera_to_bot_coordinates(location):
    with open("calibration_constants.txt", "r") as f:
        lines = f.read()
    constants = [int(x) for x in lines.split(",")]
    bot_min_x, bot_max_x, bot_bottom_y, bot_top_y, cam_min_x, cam_max_x, cam_bottom_y, cam_top_y = constants          
    x, y = location
    new_x = (x-cam_min_x) / (cam_max_x-cam_min_x) * (bot_max_x-bot_min_x) + bot_min_x
    new_y = (y-cam_bottom_y) / (cam_top_y-cam_bottom_y) * (bot_top_y-bot_bottom_y) + bot_bottom_y
    return new_x, new_y


if __name__ == "__main__":
    calibrate()