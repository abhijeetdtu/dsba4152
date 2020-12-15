var app = new Vue({
  el: '#app',
  data: {
    message: 'Hello Vue!',
    cropper: null,
    loading: false,
    same_scale:true
  },
  methods: {
    load_img_to_canvas: function() {
      var c = document.getElementById("img_canvas");
      var ctx = c.getContext("2d");
      var img = document.getElementById("img");
      ctx.drawImage(img, 0, 0, 1100, 600);
    },
    crop_img: function() {
      return this.cropper.getCroppedCanvas({
        width: 256,
        height: 256
      }).toDataURL("image/png");
    },
    create_cropper: function() {
      var image = document.getElementById('img_canvas');
      //self = this
      var preview_image = document.getElementById('preview_img');

      this.cropper = new Cropper(image, {
        aspectRatio: 1,
        crop(event) {
          // console.log(event.detail.x);
          // console.log(event.detail.y);
          // console.log(event.detail.width);
          // console.log(event.detail.height);
          // console.log(event.detail.rotate);
          // console.log(event.detail.scaleX);
          // console.log(event.detail.scaleY);
          preview_image.src = self.crop_img()
          // self.timeout = window.setTimeout(function(){
          //   if(self.timeout){
          //     window.clearTimeout(self.timeout)
          //   }
          //   self.post_image_to_server(preview_image.src)
          // },1000)
        },
      });

    },
    _update_image_src: function(id) {
      var prediction_img_a = document.getElementById(id);
      prediction_img_a.src = prediction_img_a.src + "?t=" + (new Date().getTime());
    },
    _update_predictions: function(){
      self._update_image_src('prediction_img_layer_a');
      self._update_image_src('prediction_img_layer_b');
      self.loading = false;
      // window.setTimeout(function() {
      //   self._update_image_src('prediction_img_layer_a');
      //   window.setTimeout(function() {
      //     self._update_image_src('prediction_img_layer_b');
      //     self.loading = false;
      //   }, 500);
      //
      // }, 1500)
    },
    predict: function() {
      self.loading = true;
      var preview_image = document.getElementById('preview_img');

      preview_image.src = self.crop_img()
      self.post_image_to_server(preview_image.src)
    },
    post_image_to_server: function(image_data) {
      self = this;
      data = {
        "image_data": image_data,
        "same_scale" : self.same_scale
      }
      // this.$http.post("/predict", , {emulateJSON: true})
      axios.post("/predict", data, {
        headers: {
          // Overwrite Axios's automatically set Content-Type
          'Content-Type': 'application/json'
        }
      }).then(function() {
          self._update_predictions()
      });
      // $.ajax({
      //   type: "POST",
      //   contentType: "application/json; charset=utf-8",
      //   url: "/blog/add/ajax",
      //   data: JSON.stringify({title: 'hallo', article: 'test'}),
      //   success: function (data) {
      //     console.log(data.title);
      //     console.log(data.article);
      //   },
      //   dataType: "json"
      // });
    }
  },
  mounted: function() {
    self = this
    window.setTimeout(function() {
      self.load_img_to_canvas()
      self.create_cropper()
    }, 500)

  }
})
