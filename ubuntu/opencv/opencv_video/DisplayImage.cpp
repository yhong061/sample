#include <stdio.h>
#include <vector>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/imgproc.hpp> 
#include <signal.h> 
#include <stdlib.h>  
#include <opencv2/core/core.hpp>  
#include <opencv2/highgui/highgui.hpp>  
#include <iostream>  

using namespace std;


using namespace cv;
int gRunning = 0;

//信号函数
void process(int sig)  
{  
    //cvReleaseCapture(&cam);//释放CvCapture结构  
    cout << "signal " << endl;
    gRunning = 0;
}  

void usage(int argc, char *argv[])
{
	cout << argv[0] << " video w h" <<endl;
}

int main(int argc, char *argv[])
{
	if(argc < 3) {
		usage(argc, argv);
		return 0;
	}

    double alpha =2.5;  
    double beta = 0;  
    signal(SIGINT , process);
    gRunning = 1;

	int video = atoi(argv[1]);
	int w = atoi(argv[2]);
	int h = atoi(argv[3]);

	cout << "video=" << video << " w=" << w << " h=" << h << endl;

    VideoCapture cap(video); // open the default camera
    if(!cap.isOpened())  // check if we succeeded
        return -1;

    cap.set(CV_CAP_PROP_FRAME_WIDTH,w);  
    cap.set(CV_CAP_PROP_FRAME_HEIGHT, h);  
  
    cout << "Frame Width: " << cap.get(CV_CAP_PROP_FRAME_WIDTH) << endl;  
    cout << "Frame Height: " << cap.get(CV_CAP_PROP_FRAME_HEIGHT) << endl;  
    cout << "Frame expo: " << cap.get(CV_CAP_PROP_CONTRAST) << endl;  

    Mat edges;
    Mat frame;
    namedWindow("edges",1);

    int pictureNumber = 1; 
    char SaveName[128];  

    for(;;)
    {
        Mat frame;
        Mat src;
        Mat dst;
        cap >> edges; // get a new frame from camera
        frame = edges;
        src = edges;
        imshow("edges", edges);
        waitKey(5);  //时间等待

        int a1 = edges.at<Vec3b>(2, 2)[2];  
        Vec3b b1 = edges.at<Vec3b>(2, 2)[2];  
//        cout << "访问一个数：" << a1 << " - "<<"访问三通道："<<b1<< " + ";  
        
        if(waitKey(2) == 'q') {
            sprintf(SaveName , "%5d.jpg" ,pictureNumber++);//设置图片的序号，名称  
            imwrite(SaveName , edges);//保存图片  
        }

        dst = Mat::zeros(src.size(),src.type());  
        for (int i = 0;i<src.rows;++i)  
            for(int j= 0;j<src.cols;++j)  
                for(int k = 0;k<3;++k)  
                    dst.at<Vec3b>(i,j)[k] = saturate_cast<uchar>(src.at<Vec3b>(i,j)[k]*alpha+beta);  
  
        //namedWindow("Handled Image");  
//        imshow("Handled Image",dst); 

        int a = dst.at<Vec3b>(2, 2)[2];  
        Vec3b b = dst.at<Vec3b>(2, 2)[2];  
//        cout << "访问一个数：" << a << " - "<<"访问三通道："<<b<<endl;  

//        cvtColor(frame, frame, CV_BGR2GRAY);//转化为灰度图  
//        imshow("去色", frame);  

       
//        GaussianBlur(frame, frame, Size(7, 7), 1.5, 1.5);//高斯滤波  
//        imshow("高斯滤波", frame);  
        
//        Canny(frame, frame, 60, 100);//Canny算子检测边缘，两个参数随便调  
//        imshow("Canny边缘", frame);  

        if(!gRunning) {
            cout << "exit" << endl;
            break;
        }

     //   if(waitKey(30) >= 0) break;
    }

            cout << "exited" << endl;
    cap.release();
    // the camera will be deinitialized automatically in VideoCapture destructor
    return 0;
}

int main_display_video0(int, char**)
{
    VideoCapture cap(0); // open the default camera
    if(!cap.isOpened())  // check if we succeeded
        return -1;

    Mat edges;
    namedWindow("edges",1);
    for(;;)
    {
        Mat frame;
        cap >> edges; // get a new frame from camera
        imshow("edges", edges);
        if(waitKey(30) >= 0) break;
    }
    // the camera will be deinitialized automatically in VideoCapture destructor
    return 0;
}

int main_display_video0_r_g_b(int argc,char* argv[])  
{  
    VideoCapture cap;  
    cap.open(0);  
  
    if(!cap.isOpened())   
    {  
        exit(0);  
    }  
  
    cap.set(CV_CAP_PROP_FRAME_WIDTH,250);  
    cap.set(CV_CAP_PROP_FRAME_HEIGHT,250);  
  
    cout << "Frame Width: " << cap.get(CV_CAP_PROP_FRAME_WIDTH) << endl;  
    cout << "Frame Height: " << cap.get(CV_CAP_PROP_FRAME_HEIGHT) << endl;  
  
    Mat frame;  
    vector<Mat> rgb;  
    cap >> frame;  
  
    namedWindow("original", 1);  
    namedWindow("red", 1);  
    namedWindow("green", 1);  
    namedWindow("blue", 1);  
  
    for(;;)  
    {  
        cap >> frame;  
        imshow("original", frame);  
        split(frame, rgb);  
  
        imshow("red", rgb.at(2));  
        imshow("green", rgb.at(1));  
        imshow("blue", rgb.at(0));  
  
        if(waitKey(30) >= 0)   
            break;  
    }  
  
    waitKey(0);  
    return 1;  
}  

int main_dispaly_jpg(int argc, char** argv )
{
	if ( argc != 2 )
	{
		printf("usage: DisplayImage.out <Image_Path>\n");
		return -1;
	}
	Mat image;
	image = imread( argv[1], 1 );
	if ( !image.data )
	{
		printf("No image data \n");
		return -1;
	}
	namedWindow("Display Image", WINDOW_AUTOSIZE );
	imshow("Display Image", image);
	waitKey(0);
	return 0;
}
