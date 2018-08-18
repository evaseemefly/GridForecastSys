<template>
  <div id="whole_bar" class="whole_bar_hidden">
        <div id="show_btn" class="show_btn_hidden" onclick="test()">
            点击隐藏
        </div>
        <div id="echarts_bar" ></div>
    </div>
</template>

<script>
export default {}
</script>

<style>
        #whole_bar {
            top: 100px;
            /* background: blue; */
            height: 400px;
            width: 400px;
            float: right;
            text-align: right;
        }

        #echarts_bar {
            background: #adff2f;
            height: 400px;
            width: 350px;
            float: right;
        }

        #show_btn {
            /* float: right; */
            display: inline-block;
            width: 50px;
            height: 100%;
            /* 文字垂直排列 */
            writing-mode: vertical-rl;
            /* 垂直排列居中 */
            text-align: center;
            color: white;
            /* background: red; */
            font-weight: bolder;
            font-family: "Microsoft YaHei";
            /* 设置左上及左下边角圆滑处理 */
            border-top-left-radius: 2em;
            border-bottom-left-radius: 2em;

        }
        .show_btn_hidden{
            background-color: rgb(90, 170, 216);
            transition: background-color 1.5s;
        }
        .show_btn_show{
            background-color: rgba(69, 78, 212, 0.863);
            transition: background-color 1.5s;
        }
        .whole_bar_hidden {
            position: absolute;
            height: 400px;
            width: 400px;
            animation-name: move-out;
            /*动画名称*/
            animation-duration: 1.5s;
            /* 设定动画完成后的状态 */
            animation-fill-mode: forwards;
        }
        .whole_bar_show{
            position: absolute;
            height: 400px;
            width: 400px;
            animation-name: move-in;
            /*动画名称*/
            animation-duration: 1.5s;
            /* 设定动画完成后的状态 */
            animation-fill-mode: forwards;
        }
        /* 移出效果：从左边向外部移出 */

        @keyframes move-out {
            0% {
                right: 0px;
            }
            100% {
                right: -350px;
            }
        }

        /* 渐入效果：从左边外侧移入 */

        @keyframes move-in {
            0% {
                right: -350px;
            }
            100% {
                right: 0px;
            }
        }
</style>
