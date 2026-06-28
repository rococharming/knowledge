mkdir blueos-dev
cd blueos-dev
env_path="originos-env"
if [ ! -d $env_path ]; then
  mkdir $env_path
fi

cd  $env_path

repo init -u ssh://songpengfei@smartgit:29418/VivoCode/manifests -b master -m qcom/PD2337_A_15.1.5.0.W10_blueos.xml  && repo sync -j64

cd ../


#通过查看自己负责的模块，将需要拉取的模块放入到group_names中，如：group_names=("module1" "module2" "module3");	查看自己有权限的模块参考：https://km.vivo.xyz/pages/viewpage.action?pageId=1045477496
#	模块名称    	 			|     描述
#	application  				|     应用
#	libc		 				|     libc
#	osal		 				|	  操作系统抽象层，兼容不同内核的posix接口及libc库
#	telephony					|	  通话服务
#	wcn							|	  bluetooth、nfc、wifi
#	ai							|	  ai
#	runtime						|	  运行时
#	appfwk						|	  应用框架
#	bluexlink					|	  连接
#	multimedia					|	  多媒体
#	graphic						|	  图形显示
#	blink						|	  进程间通信
#	security					|	  安全
#	common						|	  其他公共模块
# 有所有的则
group_names=("all")

group_arg=$(IFS=, ; echo "${group_names[*]}")

command="repo init -u git@gitblueos.vivo.xyz:BlueOS/manifests.git -b blueos_15_1_5_0 -m manifest.xml -g $group_arg && repo sync -j64"
echo $command
eval $command
