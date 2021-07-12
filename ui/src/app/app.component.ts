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
  velho:any;
  fokit:any;
  pbf:any;

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
    this.service.getLatestComic("velho").subscribe(data=>{
      this.velho = data;
    });
    this.service.getLatestComic("fokit").subscribe(data=>{
      this.fokit = data;
    });
    this.service.getLatestComic("pbf").subscribe(data=>{
      this.pbf = data;
    });
  }

}

