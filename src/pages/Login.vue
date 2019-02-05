<template>
  <div class="this">
    <div class="container h-100 d-flex justify-content-center align-content-center">
      <div class="row d-flex align-content-center">
        <div class="card-wrapper">
          <div class="card shadow">
            <div class="card-body">
              <h4 class="card-title pb-2">Login</h4>
              <form method="post" action="/api/login" novalidate>
                <div class="form-group">
                  <input
                    id="username"
                    type="text"
                    class="form-control"
                    name="username"
                    value
                    required
                    autofocus
                    placeholder="User name"
                  >
                  <div class="invalid-feedback">Username is invalid</div>
                </div>

                <div class="form-group">
                  <input
                    id="password"
                    type="password"
                    class="form-control"
                    name="password"
                    required
                    data-eye
                    placeholder="Password"
                  >
                  <div class="invalid-feedback">Password is required</div>
                </div>

                <div class="form-group">
                  <div class="custom-checkbox custom-control">
                    <input
                      type="checkbox"
                      name="remember"
                      id="remember"
                      class="custom-control-input"
                    >
                    <label for="remember" class="custom-control-label">Remeber Me</label>
                  </div>
                </div>

                <div class="form-group m-0">
                  <button type="submit" class="btn btn-primary btn-block">Login</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style lang="scss" scoped>
.form-control {
  background: white;
  border: 1px rgba(0, 0, 0, 0.253) solid;
  color: black !important;
  &:hover {
    background: white;
    border: 1px rgba(0, 0, 0, 0.253) solid;
  }
  &:focus {
    background: white;
  }
}
.this {
  padding-bottom: 50px;
  height: 100%;
}
</style>
