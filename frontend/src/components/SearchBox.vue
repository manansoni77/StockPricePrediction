<template>
  <div id="searchbox-container">
    <div id="searchbox">
      <input
        type="text"
        v-model="symbol"
        placeholder="Search..."
        @focus="focus = true"
      />
      <ul id="suggestionList" v-if="focus">
        <li
          v-for="option in options"
          :key="option.symbol"
          @click="selectedOption(option.symbol)"
        >
          {{ option.symbol }} - {{ option.name }}
        </li>
      </ul>
    </div>
    <b-button
      type="submit"
      variant="primary"
      @click="searchButton"
      :disabled="loading"
      >Search</b-button
    >
  </div>
</template>

<style scoped>
#searchbox-container {
  display: flex;
  margin: 0 auto;
  width: 50vw;
  min-width: 400px;
}
#searchbox-container > * {
  padding: 5px;
}
#searchbox {
  display: inline-block;
  position: relative;
}
#suggestionList {
  background-color: white;
  border: 1px solid black;
  list-style: none;
  display: block;
  margin: 0;
  padding: 0;
  width: 100%;
  overflow: hidden;
  position: absolute;
  top: 40px;
  left: 0;
  z-index: 2;
}
</style>

<script>
import { debounce } from "lodash";

export default {
  name: "SearchBox",
  props: {
    loading: Boolean,
  },
  data() {
    return {
      message: "",
      symbol: "",
      options: [],
      showAlert: false,
      focus: false,
    };
  },
  watch: {
    symbol: debounce(function () {
      this.searchOptions();
    }, 500),
  },
  methods: {
    searchButton() {
      this.focus = false;
      this.$emit("searchButtonClicked", this.symbol);
    },
    searchOptions() {
      if (this.symbol.length === 0) {
        return;
      }
      this.$axios
        .post("http://localhost:5000/search", { symbol: this.symbol })
        .then((res) => {
          if (res.status !== 200) {
            console.log("STATUS:", res.status);
          } else {
            this.options = res.data.map((option) => {
              var name = option["2. name"];
              var symbol = option["1. symbol"];
              name =
                symbol.length + name.length > 20
                  ? name.substr(0, 17 - symbol.length) + "..."
                  : name;
              return { symbol: symbol, name: name };
            });
          }
        })
        .catch((err) => {
          console.log("ERROR:", err);
        });
      console.log(this.options);
    },
    selectedOption(symbol) {
      this.symbol = symbol;
      this.focus = false;
    },
  },
};
</script>
