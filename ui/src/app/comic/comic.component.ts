import { HttpErrorResponse } from '@angular/common/http';
import { Component, Input, Output, OnInit, EventEmitter } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { throwError } from 'rxjs';
import { ComicService } from 'src/app/comic.service';

@Component({
  selector: 'app-comic',
  templateUrl: './comic.component.html',
  styleUrls: ['./comic.component.css']
})
export class ComicComponent implements OnInit {

  name:any;
  id:any;
  @Input() comic:any;
  ImageFilePath:string;

  constructor(
            private service:ComicService, 
            private route:ActivatedRoute,
            private router:Router
            ) { 
    this.ImageFilePath=this.service.ImageUrl;
  }

  ngOnInit() {
    this.route.paramMap.subscribe(params=>{
      this.name = params.get('name');
      this.id = params.get('id');
      if( this.id == null ) {
        // Id is null. 
        // Get latest comic name from 
        //   1) url param 2) comic input
        if( this.name == null ) {
          this.name = this.comic.name;
        }
        this.service.getLatestComic(this.name).subscribe(data=>{
          this.comic = data;
        });
      } else {
        // Id given as URL param. Therefore Name is in path as well.
        this.service.getComic(this.name, this.id).subscribe(data=>{
          this.comic = data;
        });
      }
    });
  }

  getComic(name:any, id:any) {
    this.service.getComic(name, id).subscribe(data=>{
      this.comic = data;
    });
  }

}
