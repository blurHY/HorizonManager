<template>
  <div>
    <div v-for="(l,i) in lines" :key="i" v-html="highlight(l)"></div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      lines: [
        "2019-01-05 06:22:55.100 | INFO     | __main__:<module>:168 - Horizon spider started",
        "2019-01-05 06:22:55.140 | WARNING  | __main__:waitForZeroHello:26 - ZeroHello has not been downloaded yet",
        "2019-01-05 06:22:55.279 | INFO     | __main__:waitForZeroHello:35 - Not downloaded.Continue waiting."
      ]
    };
  },
  methods: {
    highlight(str) {
      return str;
    }
  }
};
</script>