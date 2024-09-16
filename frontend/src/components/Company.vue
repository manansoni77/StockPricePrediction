<template>
  <div>
    <div class="company-container">
      <div class="company-data-container">
        <h2>{{ info.Name }} ( {{ info.Symbol }} )</h2>
        <br />
        {{ info.Description }}<br />
        {{ info.Industry }}<br />
        {{ info.Country }} - {{ info.Currency }} - {{ info.Exchange }}
      </div>
      <img :src="showGraph()" :key="plot" />
      <b-form @submit.prevent="sendMail">
        <b-form-group label="Get Prediction Report On Email">
          <b-form-input
            type="email"
            placeholder="Enter your email id"
            v-model="mail_id"
            required
          >
          </b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
      </b-form>
    </div>
  </div>
</template>

<style scoped>
.company-container {
  margin: 0 auto;
  padding: 15px;
  border: 5px solid black;
}

h2 {
  text-align: center;
  font-style: italic;
}
.company-data-container {
  font-weight: 500;
  font-size: large;
  text-align: left;
}

img {
  width: 800px;
}
</style>

<script>
export default {
  name: "Company",
  props: {
    info: Object,
    plot: String,
  },
  data() {
    return {
      mail_id: "",
    };
  },
  methods: {
    showGraph() {
      return "data:image/jpeg;base64," + this.plot;
    },
    sendMail() {
      this.$axios
        .post("http://localhost:5000/predict", {
          symbol: this.info.Symbol,
          mail_id: this.mail_id,
        })
        .then((res) => {
          if (res.status !== 200) {
            console.log("STATUS:", res.status);
          } else {
            console.log("success");
          }
        })
        .catch((err) => {
          console.log("ERROR:", err);
        });
    },
  },
};
</script>
