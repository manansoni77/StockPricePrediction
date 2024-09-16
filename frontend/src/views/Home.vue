<template>
  <div class="home">
    <SearchBox id="div1" @searchButtonClicked="search" :loading="loading" />
    <Company id="div2" v-if="isSuccesful" :plot="plot" :info="info" />
  </div>
</template>

<style>
.home {
  display: flex;
  flex-direction: row;
}
#div1 {
  padding: 20px;
  padding-top: 40px;
  flex-grow: 1;
}
#div2 {
  padding: 20px;
  flex-grow: 3;
}
</style>

<script>
import SearchBox from "@/components/SearchBox.vue";
import Company from "@/components/Company.vue";

export default {
  name: "Home",
  components: {
    SearchBox,
    Company,
  },
  data() {
    return {
      loading: false,
      isSuccesful: false,
      plot: "",
      info: {},
    };
  },
  methods: {
    search(symbol) {
      this.loading = true;
      this.$axios
        .post("http://localhost:5000/data", { symbol: symbol })
        .then((res) => {
          if (res.status == "200") {
            this.info = res.data.info;
            this.plot = res.data.plot;
            this.isSuccesful = true;
          } else {
            this.isSuccesful = false;
          }
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>
