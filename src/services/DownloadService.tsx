import axios from "axios";

const DownloadService = async (purpose: string) => {
  var payload = {};
  var headers = {};
  var url = "http://35.247.3.139:8001/zip/?purpose=" + purpose;
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
};

export default DownloadService;

// with open('./retrain/zip.zip', 'rb') as f:
//     st.download_button('Download Zip', f, file_name='archive.zip')
