<template>
  <div>
    <div class="line px-2 py-1" v-for="(l,i) in lines" :key="i" v-html="highlight(l)"></div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      folowTail: false
    };
  },
  watch: {
    "$root.logs"() {
      if (this.$root.logs.length > 50) this.$root.logs.shift();
      if (this.folowTail)
        this.$el.parentElement.scrollTop = this.$el.parentElement.scrollHeight;
    }
  },
  computed: {
    lines() {
      return this.$root.logs;
    }
  },
  methods: {
    highlight(str) {
      str = str.replace(/WARNING/, "<span class='text-warning'>$&</span>");
      str = str.replace(
        /DEBUG/,
        "<span class='text-info font-weight-light'>$&</span>"
      );
      str = str.replace(/INFO/, "<span class='text-info'>$&</span>");
      str = str.replace(
        /ERROR/,
        "<span class='text-danger font-weight-bold'>$&</span>"
      );
      str = str.replace(
        /CRITICAL/,
        "<span class='text-danger font-weight-bold'>$&</span>"
      );
      str = str.replace(/\s-\s(.*)$/, "&nbsp;-&nbsp;<span>$1</span>");
      str = str.replace(
        /^([0-9\s-:.])+\|/,
        "<span class='text-muted'>$&</span>"
      );
      return str;
    },
    onScroll(e) {
      this.folowTail = e.target.scrollTop == e.target.scrollHeight;
    }
  },
  sockets: {
    connect() {},
    addLogs(arr) {
      console.log("Logs addded: " + arr.length);
      this.$root.logs += arr;
    }
  },
  mounted() {
    this.$el.parentElement.addEventListener("scroll", this.onScroll);
  }
};
</script>
<style scoped>
.line:hover {
  background: rgba(0, 0, 0, 0.069);
}
.line {
  border-radius: 2px;
}
</style>
