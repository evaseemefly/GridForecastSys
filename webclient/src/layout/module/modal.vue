<template>
    <div class="modal fade" id="errorModal" tabindex="-1" role="dialog" aria-labelledby="myProgressLabel">
        <div class="modal-dialog modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h4 class="modal-title" style="font-size:29px;font-weight: 700;color:black" id="mymsgtitle">请稍后</h4>
                </div>
                <div class="modal-body">
                    <form class="form-horizontal">
                        <!--<div class="container">-->
                        <div class="bg-primary col-md-12">
                            <div id="wave_data" style="height:500px;width: 850px;">
                            </div>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-success" data-dismiss="modal">确定</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {

    }
</script>

<style>
</style>