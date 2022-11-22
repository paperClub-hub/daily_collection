<template>
    <div style="width: 100%">
      <div style="width: 1000px;text-align: left;margin: 0 auto;">
        <remote-js src="http://pv.sohu.com/cityjson?ie=utf-8"></remote-js>
        <el-button @click="getIp">获取ip</el-button>
        <p>获取到的用户ip地址：{{ ip }}</p>
      </div>
    </div>
  </template>
  <script>
  export default {
    components: {
      'remote-js': { // 获取用户ip
        render (createElement) {
          return createElement('script', {attrs: {type: 'text/javascript', src: this.src}})
        },
        props: {
          src: {type: String, required: true}
        }
      }
    },
    data () {
      return {
        ip: ''
      }
    },
    created () {
      // this.getIp()
    },
    methods: {
      getIp () {
        // eslint-disable-next-line no-undef
        this.ip = returnCitySN['cip']
        console.log('用户的ip地址：' + this.ip)
      }
    }
  }
  </script>
  <style>
    p{
      font-size: 20px;
    }
  </style>