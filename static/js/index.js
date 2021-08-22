import * as THREE from 'https://cdn.skypack.dev/three@0.131.3';
import {Water} from 'https://cdn.skypack.dev/three@0.131.3/examples/jsm/objects/Water.js';

/**
 * Three JS javascript for background water and clouds animation
 * Skills learnt from Bruno Simon ThreeJS course at 'https://threejs-journey.xyz/'
 */

// Canvas
const canvas = document.querySelector('canvas.webgl')

// Scene
const scene = new THREE.Scene()

// Water

const waterGeometry = new THREE.CircleGeometry(10000, 10000);

const water = new Water(waterGeometry, {
  textureWidth: 512,
  textureHeight: 512,
  waterNormals: new THREE.TextureLoader().load(
    "/static/img/waternormals.jpg",
    function (texture) {
      texture.wrapS = texture.wrapT = THREE.RepeatWrapping;
    }
  ),
  sunDirection: new THREE.Vector3(),
  sunColor: new THREE.Color(0x202020),
  waterColor: new THREE.Color(0x006994),
  fog: scene.fog !== undefined,
});

water.rotation.x = -Math.PI / 2;
water.position.x = -2.5;
water.position.y = 51;
water.position.z = -1710;

scene.add(water)

// Sun

const sunGeometry = new THREE.SphereGeometry(1000, 1000, 1000);
const sunMaterial = new THREE.MeshPhongMaterial({
  color: new THREE.Color(0xfce570),
  shininess: 100,
  transparent: true,
  opacity: 0.05,
});
const sun = new THREE.Mesh(sunGeometry, sunMaterial);
sun.position.x = 500;
sun.position.y = 50;
sun.position.z = -10000;
scene.add(sun);

// Clouds

let cloudArray = [];

const cloudGeometry = new THREE.PlaneGeometry(20000, 20000);
const cloudMaterial = new THREE.MeshStandardMaterial({
  map: new THREE.TextureLoader().load("/static/img/cloudimage.png"),
  transparent: true,
  opacity: 0.25,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  color: new THREE.Color(0xb68d5f),
});

for (let i = 0; i < 10; i++) {
  const cloud = new THREE.Mesh(cloudGeometry, cloudMaterial);
  cloud.position.x = (Math.random() - 0.5) * 10000;
  cloud.position.y = Math.random() * 5000;
  cloud.position.z = (Math.random() - 0.5) * 10000;
  cloud.rotation.z = Math.random() * Math.PI * 2;
  cloudArray.push(cloud);
  scene.add(cloud);
}

// Lights

const light = new THREE.AmbientLight(0xb68d5f, 1);
scene.add(light)
scene.background = new THREE.Color(0x202020)

/**
 * Sizes
 */
const sizes = {
  width: window.innerWidth,
  height: window.innerHeight
}

window.addEventListener('resize', () => {
  // Update sizes
  sizes.width = window.innerWidth
  sizes.height = window.innerHeight

  // Update camera
  camera.aspect = sizes.width / sizes.height
  camera.updateProjectionMatrix()

  // Update renderer
  renderer.setSize(sizes.width, sizes.height)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
})

/**
 * Camera
 */
// Base camera
const camera = new THREE.PerspectiveCamera(75, sizes.width / sizes.height, 0.1, 20000)
camera.position.x = 30
camera.position.y = 95
camera.position.z = 8300
scene.add(camera)

/**
 * Renderer
 */
const renderer = new THREE.WebGLRenderer({
  canvas: canvas,
})
renderer.setSize(sizes.width, sizes.height)
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))

/**
 * Animate
 */

const clock = new THREE.Clock()

const tick = () => {
  const elapsedTime = clock.getElapsedTime()

  // Cloud Movement

  cloudArray.forEach((cloud) => {
    cloud.rotation.z += 0.0005;
    cloud.opacity = Math.random();
  });

  // Water Movement

  water.material.uniforms["time"].value -= 0.002;

  // Render
  renderer.render(scene, camera)

  // Call tick again on the next frame
  window.requestAnimationFrame(tick)
}

tick()