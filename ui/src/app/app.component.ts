import { Component, OnInit } from '@angular/core';
import { ComicService } from 'src/app/comic.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {

  constructor(private service:ComicService) {     
  }

  fp:any;
  vw:any;
  xkcd:any;
  smbc:any;
  dilbert:any;

  ngOnInit(): void {
    this.service.getLatestComic("fingerpori").subscribe(data=>{
      this.fp = data;
    });
    this.service.getLatestComic("vw").subscribe(data=>{
      this.vw = data;
    });
    this.service.getLatestComic("xkcd").subscribe(data=>{
      this.xkcd = data;
    });
    this.service.getLatestComic("smbc").subscribe(data=>{
      this.smbc = data;
    });
    this.service.getLatestComic("dilbert").subscribe(data=>{
      this.dilbert = data;
    });
  }

}

