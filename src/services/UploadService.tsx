import axios from "axios";

const UploadService = async (image: any, annotation: any, purpose: string) => {
  var payload = { purpose: purpose };
  var headers = {};
  var url = "http://35.185.230.137:8001/upload/";
  var options = {
    headers: headers,
    payload: payload,
    formData: {
      image: {
        value: image.stream(),
        options: { filename: image.name, contentType: "image/*" },
      },
      annote: {
        value: annotation.stream(),
        options: { filename: annotation.name, contentType: "text/*" },
      },
    },
  };
  try {
    var res = await axios.post(url, options);
    console.log(res);
  } catch (error) {
      alert(error);
  }
};

export default UploadService;
