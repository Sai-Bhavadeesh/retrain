import axios from "axios";

const RetrainService = async (
  purpose: string,
  label: string,
  weights: string,
  epochs: number
) => {
  var payload = {};
  var headers = {};
  if (purpose in ["sizlli_bottom", "sizzli_top", "burrito"]) {
    var url =
      "http://34.105.1.34:8001/detecto/?purpose=" +
      purpose +
      "&label=" +
      label +
      "&name=" +
      weights;
    var options = {
      headers: headers,
      payload: payload,
    };
    try {
      var res = await axios.get(url, options);
      console.log(res);
    } catch (error) {
      alert(error);
    }
  } else {
    alert("Coming soon...");
  }
};

export default RetrainService;
